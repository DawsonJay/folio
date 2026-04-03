"""
Canadian Employer Test Suite — Intensive Edition

Five employer personas covering the full interview arc:
  A. Halifax Startup        – location, React, technical lead, salary
  B. Toronto AI Company     – remote, AI/ML depth, career goals, quality trade-offs
  C. Vancouver Fintech      – relocation, stakeholders, enterprise concerns
  D. Technical Screening    – debugging, architecture, testing, code craft
  E. Culture & Values       – motivation, failure, working style, self-awareness

Validates that answers:
  1. Reflect current ground truth (Halifax, IEC visa active, available now)
  2. Contain no stale pre-move / UK language
  3. Are framed consistently and employably — confident, concrete, no hedging
  4. Pass a cross-answer consistency audit for facts (years of experience, dates)

Run:  python test_canadian_employer.py
Requires: Backend API running at http://localhost:8000
"""

import re
import json
import time
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    raise

API_URL = "http://localhost:8000/api/chat"


# ---------------------------------------------------------------------------
# Employer personas
# ---------------------------------------------------------------------------

PERSONA_A = {
    "name": "Halifax Startup",
    "description": "20-person startup, hybrid 2 days/week, React/TypeScript, ~$90-110K CAD",
    "questions": [
        "Tell me about yourself",
        "Why are you in Halifax? Are you local?",
        "You're already in Canada — great. What's your work authorization status?",
        "When can you start?",
        "Walk me through your React and TypeScript experience",
        "What was your biggest accomplishment at your last job?",
        "Tell me about a project where you were technical lead",
        "What are your salary expectations?",
        "Why do you want to work at a startup rather than a large company?",
        "What do you know about Halifax's tech scene?",
    ],
}

PERSONA_B = {
    "name": "Toronto AI Company",
    "description": "Remote-first AI/ML startup, full-stack with AI focus, ~$100-130K CAD",
    "questions": [
        "What's your background?",
        "Where are you based right now?",
        "Do you need visa sponsorship?",
        "I see AI/ML on your CV — tell me about that",
        "What's your experience with RAG systems?",
        "Have you integrated LLMs into web applications?",
        "Are you open to fully remote?",
        "Why are you looking for a new role?",
        "Where do you see yourself in five years?",
        "How do you approach technical debt?",
        "Tell me about a time you had to make a trade-off between quality and speed",
    ],
}

PERSONA_C = {
    "name": "Vancouver Fintech",
    "description": "Mid-size fintech, in-office 3 days/week Vancouver, full-stack role",
    "questions": [
        "Why did you move to Canada?",
        "Are you planning to stay in Canada long-term?",
        "What's your visa situation?",
        "Can you relocate to Vancouver if needed?",
        "Tell me about your work experience",
        "How do you handle code reviews?",
        "What are you looking for in your next role?",
        "Tell me about a time you worked with non-technical stakeholders",
        "How do you handle disagreements about technical direction?",
    ],
}

PERSONA_D = {
    "name": "Technical Screening",
    "description": "Senior engineer-led screen, any company, assessing depth and craft",
    "questions": [
        "Walk me through how you approach debugging a complex production issue",
        "How do you decide when to refactor versus rewrite?",
        "Tell me about your experience with state management in React",
        "How do you approach frontend performance optimization?",
        "What's your testing philosophy?",
        "Tell me about the most technically challenging problem you've solved",
        "How do you ensure your code stays maintainable long-term?",
        "Tell me about a technical decision you made that you'd do differently now",
        "How do you stay current with new technologies?",
    ],
}

PERSONA_E = {
    "name": "Culture and Values",
    "description": "Culture fit interview — motivations, working style, self-awareness",
    "questions": [
        "What motivates you as a developer?",
        "How do you handle disagreements with teammates?",
        "Tell me about a time you failed and what you learned",
        "Describe your ideal work environment",
        "What do you do outside of work?",
        "What are your weaknesses as a developer?",
        "Why should we hire you over other candidates?",
        "What kind of problems do you find most interesting to solve?",
        "How do you handle ambiguity in a project?",
    ],
}

PERSONAS = [PERSONA_A, PERSONA_B, PERSONA_C, PERSONA_D, PERSONA_E]


# ---------------------------------------------------------------------------
# Forbidden phrases — stale UK/pre-move language that must never appear
# ---------------------------------------------------------------------------

FORBIDDEN = [
    "waiting for the visa",
    "biometrics",
    "start remotely from the uk",
    "from the uk immediately",
    "peak district",
    "planning to move to canada",
    "once the visa is active",
    "once it's active",
    "start working remotely from",
    "visa application is submitted",
    "visa to be issued",
    "i live in the uk",
    "working from the uk",
    "in the uk",
    "relocate to canada",   # already there — not relocating TO Canada
    "moving to canada",     # already done
]


# ---------------------------------------------------------------------------
# Location/immigration questions: required phrases must appear
# ---------------------------------------------------------------------------

LOCATION_KEYWORDS = [
    "visa", "work permit", "sponsorship",
    "where are you", "where in canada", "where based",
    "are you based", "are you local", "based right now",
    "are you in halifax", "based in halifax",
    "relocate", "authorization",
    "already in canada", "work authorization",
    "available immediately", "when can you start", "immigration",
]

REQUIRED_PHRASE_GROUPS = [
    # Current location
    ["halifax", "nova scotia"],
    # Visa is active (not pending)
    ["issued", "valid", "active"],
    # No sponsorship burden
    [
        "no sponsorship", "no employer sponsorship", "without sponsorship",
        "no work permit sponsorship", "doesn't require", "does not require",
        "no visa sponsorship",
    ],
]


# ---------------------------------------------------------------------------
# Red-flag patterns — general employability issues
# ---------------------------------------------------------------------------

PRESCRIPTIVE_PATTERNS = [
    r"\bthis demonstrates\b",
    r"\bthis proves\b",
    r"\bthis shows\b",
    r"\bmy superpower is\b",
    r"\bthe proof is in\b",
    r"\bwhat makes me unique is\b",
    r"\bwhat sets me apart\b",
]

# Checked against the first 200 characters of the answer
DEFENSIVE_OPENER_PATTERNS = [
    r"\bi('m| am) currently unemployed\b",
    r"\bunemployed\b",
    r"\bi('m| am) not sure (if|whether|that|how)\b",
    r"\bunfortunately\b",
    r"\bi don't really have\b",
    r"\bi haven't (really|actually|done|built)\b",
    r"\bi lack\b",
]

# Hedging that undermines confident professional framing
HEDGING_PATTERNS = [
    r"\bi think i (might|could|can|should)\b",
    r"\bi('m| am) trying to\b",
    r"\bi('m| am) hoping to\b",
    r"\bi('d| would) like to think\b",
    r"\bi guess\b",
    r"\bi('m| am) kind of\b",
    r"\bmaybe i\b",
    r"\bi can't really\b",
    r"\bi don't really know\b",
]

SALARY_RE = re.compile(
    r"(\$\s?\d{2,3}[kK]?|\d{2,3}\s?[kK]\s?(cad|CAD)|\d{2,3},?\d{3})",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Known wrong facts — if these appear anywhere, flag as inconsistency
# ---------------------------------------------------------------------------

WRONG_FACTS = [
    # Experience duration
    ("six years of", "experience should be stated as 5.5 years"),
    ("6 years of experience", "experience should be stated as 5.5 years"),
    ("five years of experience", "experience is 5.5 years — undersells by a year"),
    # Nurtur tenure
    ("4 years at nurtur", "Nurtur was 3.5 years (July 2022 – Feb 2026)"),
    ("four years at nurtur", "Nurtur was 3.5 years (July 2022 – Feb 2026)"),
    ("2 years at nurtur", "Nurtur was 3.5 years (July 2022 – Feb 2026)"),
    ("two years at nurtur", "Nurtur was 3.5 years (July 2022 – Feb 2026)"),
    # Date errors
    ("july 2021", "Nurtur started July 2022, not 2021"),
    ("january 2026", "role ended February 2026, not January"),
    ("december 2025", "role ended February 2026, not December 2025"),
    # Location errors
    ("based in the uk", "should be Halifax, Nova Scotia"),
    ("living in the uk", "should be Halifax, Nova Scotia"),
    ("currently in the uk", "should be Halifax, Nova Scotia"),
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def word_count(text: str) -> int:
    return len(text.split())


def is_location_question(question: str) -> bool:
    q = question.lower()
    return any(kw in q for kw in LOCATION_KEYWORDS)


def check_wrong_facts(answer_lower: str) -> list[str]:
    hits = []
    for phrase, reason in WRONG_FACTS:
        if phrase in answer_lower:
            hits.append(f"Wrong fact: '{phrase}' — {reason}")
    return hits


# ---------------------------------------------------------------------------
# Per-answer checking
# ---------------------------------------------------------------------------

def check_answer(question: str, answer: str) -> dict:
    """
    Returns:
      forbidden_hits  – stale/bad phrases found
      required_misses – required groups missing on location questions
      red_flags       – employability issues (length, hedging, etc.)
      pass_fail       – PASS | WARN | FAIL
    """
    a_lower = answer.lower()
    first_200 = answer[:200].lower()

    # 1. Forbidden phrase check
    forbidden_hits = [p for p in FORBIDDEN if p in a_lower]

    # 2. Required phrases on location/immigration questions
    required_misses = []
    if is_location_question(question):
        for group in REQUIRED_PHRASE_GROUPS:
            if not any(p in a_lower for p in group):
                required_misses.append(group[0])

    # 3. Red flags
    red_flags = []

    for pat in PRESCRIPTIVE_PATTERNS:
        if re.search(pat, a_lower):
            red_flags.append("Prescriptive language (tells reader what to conclude)")
            break

    wc = word_count(answer)
    if wc > 350:
        red_flags.append(f"Too long ({wc} words — loses attention)")
    if wc < 40:
        red_flags.append(f"Too short ({wc} words — no concrete content)")

    # Defensive opener (first 200 chars only)
    for pat in DEFENSIVE_OPENER_PATTERNS:
        if re.search(pat, first_200):
            red_flags.append(f"Defensive opener: matches '{pat}'")
            break

    # Hedging language (whole answer — count matches)
    hedging_hits = [pat for pat in HEDGING_PATTERNS if re.search(pat, a_lower)]
    if len(hedging_hits) >= 2:
        red_flags.append(f"Excessive hedging ({len(hedging_hits)} patterns: confidence undermined)")

    # Salary question must include a number
    if "salary" in question.lower():
        if not SALARY_RE.search(answer):
            red_flags.append("Salary question answered without a concrete number/range")

    # Wrong facts
    wrong = check_wrong_facts(a_lower)
    red_flags.extend(wrong)

    # Determine pass/fail/warn
    if forbidden_hits or red_flags:
        pass_fail = "FAIL"
    elif required_misses:
        pass_fail = "WARN"
    else:
        pass_fail = "PASS"

    return {
        "forbidden_hits": forbidden_hits,
        "required_misses": required_misses,
        "red_flags": red_flags,
        "pass_fail": pass_fail,
        "word_count": wc,
    }


# ---------------------------------------------------------------------------
# Cross-answer consistency audit
# ---------------------------------------------------------------------------

def consistency_audit(all_results: list[dict]) -> list[str]:
    """
    Scan ALL answers collectively for consistency issues:
    - Location should always be Halifax (never UK)
    - Years of experience should be consistent (~5.5)
    - Nurtur tenure should be consistent (3.5 years)
    """
    issues = []

    # Combine all answer text with question context for reporting
    for r in all_results:
        a_lower = r["answer"].lower()
        q = r["question"]

        # Already caught per-answer — but flag any remaining UK location
        if re.search(r"\b(based|living|located|working)\s+in\s+the\s+uk\b", a_lower):
            issues.append(
                f"[{r['persona']}] '{q[:50]}' — claims UK location"
            )

        # Check for inconsistent years of experience
        # Valid: "5.5 years", "five and a half years", "five point five"
        # Invalid if mentions a specific year count that's clearly wrong
        for phrase, reason in WRONG_FACTS:
            if phrase in a_lower:
                issues.append(
                    f"[{r['persona']}] '{q[:50]}' — {reason}"
                )

    # Deduplicate
    return list(dict.fromkeys(issues))


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def ask_api(question: str, session_id: str) -> dict:
    try:
        r = requests.post(
            API_URL,
            json={"question": question, "session_id": session_id},
            timeout=30,
        )
        r.raise_for_status()
        d = r.json()
        return {
            "answer": d.get("answer", ""),
            "confidence": d.get("confidence", ""),
            "score": float(d.get("top_score") or 0),
        }
    except Exception as e:
        return {
            "answer": f"ERROR: {e}",
            "confidence": "error",
            "score": 0.0,
        }


# ---------------------------------------------------------------------------
# Run a full persona interview
# ---------------------------------------------------------------------------

def run_persona(persona: dict, session_id: str) -> list[dict]:
    results = []
    for question in persona["questions"]:
        api = ask_api(question, session_id)
        checks = check_answer(question, api["answer"])
        results.append({
            "persona": persona["name"],
            "question": question,
            "answer": api["answer"],
            "answer_preview": api["answer"][:250] + ("..." if len(api["answer"]) > 250 else ""),
            "confidence": api["confidence"],
            "score": round(api["score"], 3),
            **checks,
        })
        time.sleep(0.4)
    return results


# ---------------------------------------------------------------------------
# Print helpers
# ---------------------------------------------------------------------------

PASS_LABEL = "[PASS]"
WARN_LABEL = "[WARN]"
FAIL_LABEL = "[FAIL]"


def label(pf: str) -> str:
    return {"PASS": PASS_LABEL, "WARN": WARN_LABEL, "FAIL": FAIL_LABEL}.get(pf, pf)


def print_persona_header(persona: dict) -> None:
    print()
    print("=" * 72)
    print(f"  PERSONA: {persona['name']}")
    print(f"  {persona['description']}")
    print("=" * 72)


def print_result(i: int, r: dict) -> None:
    lbl = label(r["pass_fail"])
    print(f"\n  Q{i}. {r['question']}")
    print(f"  {lbl}  conf={r['confidence']}  score={r['score']}  words={r['word_count']}")
    print(f"  > {r['answer_preview']}")
    for h in r["forbidden_hits"]:
        print(f"      [!] FORBIDDEN: \"{h}\"")
    for m in r["required_misses"]:
        print(f"      [?] REQUIRED MISSING: \"{m}\" group not found")
    for f in r["red_flags"]:
        print(f"      [!] RED FLAG: {f}")


# ---------------------------------------------------------------------------
# Summarise
# ---------------------------------------------------------------------------

def summarise(all_results: list[dict]) -> dict:
    total   = len(all_results)
    passes  = sum(1 for r in all_results if r["pass_fail"] == "PASS")
    warns   = sum(1 for r in all_results if r["pass_fail"] == "WARN")
    fails   = sum(1 for r in all_results if r["pass_fail"] == "FAIL")

    total_forbidden      = sum(len(r["forbidden_hits"])   for r in all_results)
    total_required_miss  = sum(len(r["required_misses"])  for r in all_results)
    total_red_flags      = sum(len(r["red_flags"])        for r in all_results)

    failed_qs  = [r["question"] for r in all_results if r["pass_fail"] == "FAIL"]
    warned_qs  = [r["question"] for r in all_results if r["pass_fail"] == "WARN"]

    consistency_issues = consistency_audit(all_results)

    # Verdict — scaled for ~48 questions (allow slightly more WARNs than v1)
    if fails == 0 and warns == 0 and not consistency_issues:
        verdict      = "STRONG"
        verdict_note = "Clean across all five personas. Would move to next round."
    elif fails == 0 and warns <= 3 and not consistency_issues:
        verdict      = "SOLID"
        verdict_note = f"{warns} WARN(s) — minor phrasing gaps, no real blockers."
    elif fails <= 2 and not consistency_issues:
        verdict      = "CONCERNS"
        verdict_note = f"{fails} FAIL(s) require fixes before sending."
    else:
        verdict      = "FAIL"
        verdict_note = (
            f"{fails} FAIL(s)" +
            (f" + {len(consistency_issues)} consistency issue(s)" if consistency_issues else "") +
            " — significant rework needed."
        )

    return {
        "total": total,
        "passes": passes,
        "warns": warns,
        "fails": fails,
        "total_forbidden_hits": total_forbidden,
        "total_required_misses": total_required_miss,
        "total_red_flags": total_red_flags,
        "failed_questions": failed_qs,
        "warned_questions": warned_qs,
        "consistency_issues": consistency_issues,
        "verdict": verdict,
        "verdict_note": verdict_note,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print()
    print("=" * 72)
    print("  CANADIAN EMPLOYER TEST SUITE — INTENSIVE EDITION")
    print("  5 personas | location + technical + behavioral + culture + values")
    print("  Checks: stale language | framing | consistency | employability")
    print("=" * 72)

    all_results = []

    for persona in PERSONAS:
        print_persona_header(persona)
        session_id = (
            f"employer-test-{persona['name'].lower().replace(' ', '-')}"
            f"-{int(time.time())}"
        )
        results = run_persona(persona, session_id)
        all_results.extend(results)
        for i, r in enumerate(results, 1):
            print_result(i, r)

    summary = summarise(all_results)

    print()
    print("=" * 72)
    print("  SUMMARY")
    print("=" * 72)
    print(f"  Total questions     : {summary['total']}")
    print(f"  PASS                : {summary['passes']}")
    print(f"  WARN                : {summary['warns']}  (missing expected phrases)")
    print(f"  FAIL                : {summary['fails']}  (stale language or red flags)")
    print(f"  Forbidden hits      : {summary['total_forbidden_hits']}")
    print(f"  Red flags           : {summary['total_red_flags']}")

    if summary["consistency_issues"]:
        print()
        print("  CONSISTENCY ISSUES:")
        for issue in summary["consistency_issues"]:
            print(f"    [!] {issue}")
    else:
        print(f"  Consistency audit   : CLEAN")

    if summary["failed_questions"]:
        print()
        print("  Failed questions:")
        for q in summary["failed_questions"]:
            print(f"    [FAIL] {q}")

    if summary["warned_questions"]:
        print()
        print("  Warned questions:")
        for q in summary["warned_questions"]:
            print(f"    [WARN] {q}")

    print()
    print("=" * 72)
    print(f"  VERDICT: {summary['verdict']}")
    print(f"  {summary['verdict_note']}")
    print("=" * 72)

    # Save JSON report
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_file = f"canadian_employer_test_{timestamp}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": timestamp,
                "summary": summary,
                "results": [
                    {k: v for k, v in r.items() if k != "answer"}
                    for r in all_results
                ],
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"\n  Results saved: {report_file}")


if __name__ == "__main__":
    main()
