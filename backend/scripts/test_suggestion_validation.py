"""
Suggestion Validation Test
==========================
Phase 1 (structural, no API calls): validates the service layer.
Phase 2 (live, requires backend on localhost:8000): validates LLM compliance.

Usage:
  # Phase 1 only (fast):
  python scripts/test_suggestion_validation.py

  # Both phases (requires running backend):
  python scripts/test_suggestion_validation.py --live
"""

import sys
import json
import time
import argparse
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from app.services.direct_answer_service import DirectAnswerService

API_URL = "http://localhost:8000/api/chat"
DIRECT_ANSWERS_DIR = Path(__file__).parent.parent / "notes" / "tier-1-direct-answers"
EMBEDDINGS_FILE = Path(__file__).parent.parent / "direct-answer-embeddings.json"

# ── Hardcoded suggestion lists (copied from source — test fails if these drift) ──

INITIAL_SUGGESTIONS = [
    "What is Folio?",
    "Tell me about your current experience",
    "Why are you looking for a new role?",
    "What are your strongest technical skills?",
    "What project are you most proud of?",
    "What are you looking for in your next role?",
]

OFF_TOPIC_SUGGESTIONS = [
    "Tell me about yourself",
    "What are your strongest technical skills?",
    "What projects have you built?",
    "Why are you looking for a new role?",
    "How do you approach problem-solving?",
    "How did you transition from art to tech?",
]

BOUNDARY_SUGGESTIONS = [
    "What is Folio?",
    "What's your experience with RAG systems?",
    "Do you have experience with LLMs?",
    "What AI/ML experience do you have?",
    "What are your strongest technical skills?",
    "Tell me about yourself",
]

# ── Live test questions spanning all confidence paths ──

LIVE_QUESTIONS = [
    # Direct answer path (known high-scoring matches)
    "Tell me about yourself",
    "Do you know C#?",
    "Are you willing to relocate?",
    # High-confidence RAG
    "What Python frameworks have you used?",
    "Tell me about your frontend development experience",
    # Medium / redirect
    "What's your story?",
    "Tell me more about your background",
]


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def header(text: str) -> None:
    print()
    print("=" * 70)
    print(text)
    print("=" * 70)


def subheader(text: str) -> None:
    print(f"\n{text}")
    print("-" * len(text))


def ok(msg: str) -> None:
    print(f"  OK  {msg}")


def fail(msg: str) -> None:
    print(f"  FAIL {msg}")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 1
# ─────────────────────────────────────────────────────────────────────────────

def check_hardcoded_suggestions(known_titles: set) -> bool:
    subheader("Check 1: Hardcoded suggestions are valid index entries")

    all_passed = True
    groups = {
        "INITIAL_SUGGESTIONS": INITIAL_SUGGESTIONS,
        "off_topic": OFF_TOPIC_SUGGESTIONS,
        "boundary": BOUNDARY_SUGGESTIONS,
    }

    for name, suggestions in groups.items():
        invalid = [s for s in suggestions if s not in known_titles]
        total = len(suggestions)
        if invalid:
            fail(f"{name} ({total - len(invalid)}/{total}) — INVALID: {invalid}")
            all_passed = False
        else:
            ok(f"{name} ({total}/{total})")

    return all_passed


def check_resolve_suggestions(svc: DirectAnswerService, index: list) -> bool:
    subheader("Check 2: _resolve_suggestions correctness")

    # Find a shortTitle that differs from its fullTitle
    short_entry = next((e for e in index if e["shortTitle"] != e["fullTitle"]), None)
    # Find a full-title entry (shortTitle == fullTitle)
    full_entry = next((e for e in index if e["shortTitle"] == e["fullTitle"]), None)

    if not short_entry or not full_entry:
        fail("Could not find suitable test entries in index")
        return False

    inputs = [
        short_entry["shortTitle"],   # should get query = fullTitle
        full_entry["shortTitle"],    # should NOT have query
        "This string is not in the index at all",  # unknown — no query, text only
    ]

    result = svc._resolve_suggestions(inputs, index, "test")

    passed = True

    # Short entry: must have text and query
    r0 = result[0]
    if r0.get("text") == short_entry["shortTitle"] and r0.get("query") == short_entry["fullTitle"]:
        ok(f"shortTitle '{short_entry['shortTitle']}' -> query='{short_entry['fullTitle']}'")
    else:
        fail(f"shortTitle resolution wrong: got {r0}")
        passed = False

    # Full entry: must have text only, no query
    r1 = result[1]
    if r1.get("text") == full_entry["shortTitle"] and "query" not in r1:
        ok(f"fullTitle '{full_entry['shortTitle']}' -> no query field (correct)")
    else:
        fail(f"fullTitle resolution wrong: got {r1}")
        passed = False

    # Unknown: text only, no query
    r2 = result[2]
    if r2.get("text") == inputs[2] and "query" not in r2:
        ok(f"unknown string -> fallback to text only (correct)")
    else:
        fail(f"unknown string resolution wrong: got {r2}")
        passed = False

    return passed


def check_query_values_in_embeddings(index: list) -> bool:
    subheader("Check 3: query (fullTitle) values match embeddings store")

    if not EMBEDDINGS_FILE.exists():
        fail(f"Embeddings file not found: {EMBEDDINGS_FILE}")
        return False

    with open(EMBEDDINGS_FILE, encoding="utf-8") as f:
        emb_data = json.load(f)

    stored_questions = {v["metadata"]["question"] for v in emb_data.values()}

    short_entries = [e for e in index if e["shortTitle"] != e["fullTitle"]]
    missing = [e for e in short_entries if e["fullTitle"] not in stored_questions]

    if missing:
        fail(f"{len(missing)} fullTitle(s) NOT found in embeddings store:")
        for e in missing:
            print(f"    shortTitle: {e['shortTitle']}")
            print(f"    fullTitle:  {e['fullTitle']}")
        return False

    ok(f"{len(short_entries)} shortTitle entries checked — all fullTitles found in embeddings")
    return True


def check_direct_answer_file_suggestions(svc: DirectAnswerService, known_titles: set) -> bool:
    subheader("Check 4: All direct answer file suggestions are valid")

    md_files = sorted(DIRECT_ANSWERS_DIR.glob("*.md"))
    total_files = 0
    total_suggestions = 0
    failures = []

    for md_file in md_files:
        try:
            rel_path = f"notes/tier-1-direct-answers/{md_file.name}"
            result = svc.load_direct_answer(rel_path)
            total_files += 1
            for s in result["suggestions"]:
                text = s.get("text", "")
                total_suggestions += 1
                if text not in known_titles:
                    failures.append((md_file.name, text))
        except Exception as e:
            failures.append((md_file.name, f"ERROR: {e}"))

    if failures:
        fail(f"{total_files} files, {total_suggestions} suggestions — {len(failures)} INVALID:")
        for fname, text in failures[:20]:
            print(f"    [{fname}] '{text}'")
        if len(failures) > 20:
            print(f"    ... and {len(failures) - 20} more")
        return False

    ok(f"{total_files} files, {total_suggestions} suggestions — all valid")
    return True


def run_phase_1() -> int:
    header("PHASE 1: STRUCTURAL VALIDATION")

    svc = DirectAnswerService()
    index = svc.get_index()
    known_titles = {e["shortTitle"] for e in index}

    results = [
        check_hardcoded_suggestions(known_titles),
        check_resolve_suggestions(svc, index),
        check_query_values_in_embeddings(index),
        check_direct_answer_file_suggestions(svc, known_titles),
    ]

    passed = sum(1 for r in results if r)
    total = len(results)
    return passed, total


# ─────────────────────────────────────────────────────────────────────────────
# Phase 2
# ─────────────────────────────────────────────────────────────────────────────

def validate_response_suggestions(suggestions: list, index_map: dict) -> list:
    """
    Returns list of failure strings. Empty list = all valid.
    index_map: shortTitle -> fullTitle
    """
    failures = []
    for i, s in enumerate(suggestions):
        text = s.get("text", "")
        query = s.get("query")

        if text not in index_map:
            failures.append(f"  suggestion[{i}] text='{text}' is NOT in the shortTitle index")
            continue

        expected_full = index_map[text]
        if expected_full != text:
            # Should have a query field set to fullTitle
            if query is None:
                failures.append(
                    f"  suggestion[{i}] text='{text}' is a shortTitle but missing query field"
                    f" (expected query='{expected_full}')"
                )
            elif query != expected_full:
                failures.append(
                    f"  suggestion[{i}] text='{text}' has wrong query='{query}'"
                    f" (expected '{expected_full}')"
                )
        else:
            # Full title — query should be absent or equal to text
            if query is not None and query != text:
                failures.append(
                    f"  suggestion[{i}] text='{text}' is a full title but has unexpected query='{query}'"
                )

    return failures


def run_phase_2(svc: DirectAnswerService) -> tuple:
    header("PHASE 2: LIVE VALIDATION")

    if not REQUESTS_AVAILABLE:
        print("  SKIP: 'requests' library not installed (pip install requests)")
        return 0, 0

    index = svc.get_index()
    index_map = {e["shortTitle"]: e["fullTitle"] for e in index}

    questions_passed = 0
    questions_total = 0

    for i, question in enumerate(LIVE_QUESTIONS, 1):
        print(f"\n[{i}/{len(LIVE_QUESTIONS)}] \"{question}\"")
        try:
            start = time.time()
            resp = requests.post(
                API_URL,
                json={"question": question},
                headers={"Content-Type": "application/json"},
                timeout=60,
            )
            elapsed = int((time.time() - start) * 1000)

            if resp.status_code != 200:
                fail(f"HTTP {resp.status_code}: {resp.text[:200]}")
                questions_total += 1
                continue

            data = resp.json()
            confidence = data.get("confidence", "?")
            top_score = data.get("top_score", 0.0)
            suggestions = data.get("suggestions", [])

            with_query = sum(1 for s in suggestions if s.get("query"))
            print(f"  confidence={confidence}, score={top_score:.4f}, {elapsed}ms")
            print(f"  suggestions: {len(suggestions)} returned, {with_query} with query field")

            failures = validate_response_suggestions(suggestions, index_map)
            questions_total += 1

            if failures:
                fail(f"{len(failures)} invalid suggestion(s):")
                for f_msg in failures:
                    print(f_msg)
            else:
                valid_count = len(suggestions)
                ok(f"{valid_count}/6 valid")
                questions_passed += 1

        except requests.exceptions.ConnectionError:
            print("  SKIP: backend not reachable at localhost:8000")
            break
        except Exception as e:
            fail(f"Unexpected error: {e}")
            questions_total += 1

    return questions_passed, questions_total


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Suggestion validation test")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Also run Phase 2 live endpoint tests (requires backend on localhost:8000)",
    )
    args = parser.parse_args()

    structural_passed, structural_total = run_phase_1()

    live_passed = live_total = 0
    if args.live:
        svc = DirectAnswerService()
        live_passed, live_total = run_phase_2(svc)

    header("SUMMARY")
    print(f"  Structural: {structural_passed}/{structural_total} checks passed")
    if args.live:
        if live_total > 0:
            print(f"  Live:       {live_passed}/{live_total} questions had all-valid suggestions")
        else:
            print("  Live:       skipped (backend not reachable)")

    all_structural_ok = structural_passed == structural_total
    all_live_ok = (not args.live) or (live_total > 0 and live_passed == live_total)

    if all_structural_ok and all_live_ok:
        print("\n  ALL CHECKS PASSED")
        sys.exit(0)
    else:
        print("\n  SOME CHECKS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
