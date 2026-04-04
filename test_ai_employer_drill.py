"""
AI-Forward Canadian Employer Test — Conversational Deep-Drill Edition

Persona: CTO / Senior Engineering Manager at a growing Canadian tech company
         (50-200 employees) that is actively building AI features into their
         SaaS platform. Looking for a senior web developer who can both ship
         reliable React/TypeScript code AND own AI feature integration
         (LLMs, RAG, embeddings) end-to-end.

What makes this test different from the standard employer test:
  1. Single continuous interview arc — one employer, one conversation.
  2. After designated questions, the test inspects the API's returned
     suggestions and selects the most AI/technically-relevant follow-up
     question. This drills deeper into interesting threads the way a real
     interviewer would, and also validates that the suggestion system is
     producing useful interview leads.
  3. After all questions, the full Q&A transcript is printed clearly and
     saved to JSON for manual review and assessment.

Run:  python test_ai_employer_drill.py
Requires: Backend API running at http://localhost:8000
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

# Ensure UTF-8 output on Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    raise

API_URL = "http://localhost:8000/api/chat"
SESSION_ID = f"ai-employer-drill-{int(time.time())}"


# ---------------------------------------------------------------------------
# Persona
# ---------------------------------------------------------------------------

PERSONA = {
    "name": "Canadian AI-Forward Tech Company",
    "role": "Senior Web Developer - AI Features",
    "description": (
        "Growing Canadian SaaS company (50-200 employees) actively building AI features "
        "into their platform. The interviewer is a CTO or Senior Engineering Manager. "
        "They want a senior web developer who can ship reliable React/TypeScript code "
        "AND own the integration of LLMs, RAG, and embeddings into production. "
        "They are looking for someone who can grow into a technical leadership role."
    ),
}


# ---------------------------------------------------------------------------
# Interview questions — grouped by section
# drill=True means: after this question, pick the best suggestion and ask it
# ---------------------------------------------------------------------------

INTERVIEW_SECTIONS = [
    {
        "section": "Opening",
        "drill": False,
        "questions": [
            "Tell me about yourself",
            "What draws you to working on AI features in a product?",
            "What's your work authorization status in Canada?",
        ],
    },
    {
        "section": "Technical Depth",
        "drill": True,
        "questions": [
            "Walk me through your React and TypeScript experience",
            "Tell me about the most technically challenging problem you've solved",
        ],
    },
    {
        "section": "AI and LLM Focus",
        "drill": True,
        "questions": [
            "I see AI/ML on your CV — tell me about your production AI experience",
            "How would you approach adding a new LLM-powered feature to an existing web application?",
            "What's your experience with RAG systems and prompt engineering?",
        ],
    },
    {
        "section": "Senior Role Fit",
        "drill": False,
        "questions": [
            "Tell me about a time you were the technical lead on a project",
            "How do you balance shipping fast with keeping code quality high?",
            "What kind of technical problems do you find most interesting to solve?",
        ],
    },
    {
        "section": "Culture and Fit",
        "drill": False,
        "questions": [
            "What's your biggest weakness as a developer?",
            "Why should we hire you for this role — what makes you stand out?",
        ],
    },
]


# ---------------------------------------------------------------------------
# Suggestion selection
# Keywords that signal AI or technical depth — used to score suggestions
# ---------------------------------------------------------------------------

AI_KEYWORDS = [
    "ai", "ml", "llm", "rag", "model", "openai", "embedding", "prompt",
    "machine learning", "langchain", "vector", "gpt", "recommendation",
    "intelligent", "automation", "neural", "chatbot", "context window",
]

TECHNICAL_KEYWORDS = [
    "performance", "architecture", "debug", "scale", "optimiz", "test",
    "typescript", "react", "backend", "api", "database", "refactor",
    "design pattern", "technical decision", "production", "system",
]


def score_suggestion(text: str) -> int:
    t = text.lower()
    score = 0
    for kw in AI_KEYWORDS:
        if kw in t:
            score += 3
    for kw in TECHNICAL_KEYWORDS:
        if kw in t:
            score += 1
    return score


def pick_drill_question(suggestions: list) -> Optional[str]:
    """Return the suggestion most relevant to AI/technical depth, or None."""
    if not suggestions:
        return None
    scored = []
    for s in suggestions:
        text = s.get("text", s) if isinstance(s, dict) else str(s)
        scored.append((score_suggestion(text), text))
    scored.sort(key=lambda x: x[0], reverse=True)
    # Only drill if there's a genuinely relevant suggestion (score > 0)
    if scored[0][0] == 0:
        return None
    return scored[0][1]


# ---------------------------------------------------------------------------
# API helper
# ---------------------------------------------------------------------------

def ask_api(question: str) -> dict:
    try:
        r = requests.post(
            API_URL,
            json={"question": question, "session_id": SESSION_ID},
            timeout=30,
        )
        r.raise_for_status()
        d = r.json()
        return {
            "answer": d.get("answer", ""),
            "suggestions": d.get("suggestions", []),
            "confidence": d.get("confidence", "unknown"),
            "score": float(d.get("top_score") or 0),
            "error": None,
        }
    except Exception as e:
        return {
            "answer": f"ERROR: {e}",
            "suggestions": [],
            "confidence": "error",
            "score": 0.0,
            "error": str(e),
        }


# ---------------------------------------------------------------------------
# Interview runner
# ---------------------------------------------------------------------------

def run_interview() -> list[dict]:
    """Run the full interview arc with suggestion-driven drill-downs."""
    all_results = []
    q_num = 0

    for section_cfg in INTERVIEW_SECTIONS:
        section = section_cfg["section"]
        drill_enabled = section_cfg["drill"]

        print(f"\n{'='*70}")
        print(f"  {section.upper()}")
        print(f"{'='*70}")

        for question in section_cfg["questions"]:
            q_num += 1
            print(f"\n  Q{q_num}. {question}")

            response = ask_api(question)
            wc = len(response["answer"].split())
            preview = response["answer"][:250] + ("..." if len(response["answer"]) > 250 else "")

            print(f"  conf={response['confidence']}  score={response['score']}  words={wc}")
            print(f"  > {preview}")

            all_results.append({
                "section": section,
                "q_num": q_num,
                "question": question,
                "answer": response["answer"],
                "answer_preview": preview,
                "confidence": response["confidence"],
                "score": round(response["score"], 3),
                "word_count": wc,
                "is_drill": False,
                "drill_from": None,
                "suggestions_returned": [
                    (s.get("text", s) if isinstance(s, dict) else str(s))
                    for s in response["suggestions"]
                ],
                "error": response["error"],
            })

            # Drill down if this section supports it and the answer was good
            if drill_enabled and not response["error"] and not response["answer"].startswith("ERROR:"):
                drill_q = pick_drill_question(response["suggestions"])
                if drill_q:
                    q_num += 1
                    print(f"\n  Q{q_num}. [DRILL from suggestions] {drill_q}")

                    drill_resp = ask_api(drill_q)
                    drill_wc = len(drill_resp["answer"].split())
                    drill_preview = drill_resp["answer"][:250] + ("..." if len(drill_resp["answer"]) > 250 else "")

                    print(f"  conf={drill_resp['confidence']}  score={drill_resp['score']}  words={drill_wc}")
                    print(f"  > {drill_preview}")

                    all_results.append({
                        "section": section,
                        "q_num": q_num,
                        "question": drill_q,
                        "answer": drill_resp["answer"],
                        "answer_preview": drill_preview,
                        "confidence": drill_resp["confidence"],
                        "score": round(drill_resp["score"], 3),
                        "word_count": drill_wc,
                        "is_drill": True,
                        "drill_from": question,
                        "suggestions_returned": [
                            (s.get("text", s) if isinstance(s, dict) else str(s))
                            for s in drill_resp["suggestions"]
                        ],
                        "error": drill_resp["error"],
                    })

            time.sleep(0.4)

    return all_results


# ---------------------------------------------------------------------------
# Summary stats
# ---------------------------------------------------------------------------

def summarise(results: list[dict]) -> dict:
    successful = [
        r for r in results
        if not r.get("error") and not r["answer"].startswith("ERROR:")
    ]
    errors = [r for r in results if r.get("error") or r["answer"].startswith("ERROR:")]
    drills = [r for r in results if r.get("is_drill")]

    avg_score = sum(r["score"] for r in successful) / len(successful) if successful else 0
    avg_words = sum(r["word_count"] for r in successful) / len(successful) if successful else 0

    confidence_dist: dict[str, int] = {}
    for r in successful:
        c = r["confidence"]
        confidence_dist[c] = confidence_dist.get(c, 0) + 1

    return {
        "total_questions": len(results),
        "successful_responses": len(successful),
        "error_responses": len(errors),
        "drill_questions_asked": len(drills),
        "avg_confidence_score": round(avg_score, 3),
        "avg_word_count": round(avg_words),
        "confidence_distribution": confidence_dist,
        "sections": list({r["section"] for r in results}),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def print_transcript(results: list[dict]) -> None:
    """Print the full Q&A transcript clearly for manual review."""
    print("\n\n" + "=" * 70)
    print("  FULL INTERVIEW TRANSCRIPT")
    print("=" * 70)

    current_section = None
    for r in results:
        if r["section"] != current_section:
            current_section = r["section"]
            print(f"\n-- {current_section.upper()} {'-' * (60 - len(current_section))}")

        drill_marker = "  [DRILL]" if r.get("is_drill") else ""
        print(f"\nQ{r['q_num']}{drill_marker}: {r['question']}")
        print(f"conf={r['confidence']}  score={r['score']}  words={r['word_count']}")
        print()

        if r.get("error") or r["answer_preview"].startswith("ERROR:"):
            print(f"  ERROR: {r.get('error', r['answer_preview'])}")
        else:
            # Print full answer (from the saved answer field if available)
            answer_text = r.get("answer", r["answer_preview"])
            for line in answer_text.split("\n"):
                print(f"  {line}")

        print()


def main():
    print()
    print("=" * 70)
    print("  AI-FORWARD CANADIAN EMPLOYER TEST")
    print("  Conversational Deep-Drill Edition")
    print(f"  Persona : {PERSONA['name']}")
    print(f"  Role    : {PERSONA['role']}")
    print("  Mode    : Fixed questions + suggestion-driven drill-downs")
    print(f"  Session : {SESSION_ID}")
    print("=" * 70)

    # Run the interview
    results = run_interview()

    # Statistics
    summary = summarise(results)

    print("\n\n" + "=" * 70)
    print("  STATISTICS")
    print("=" * 70)
    print(f"  Total questions asked : {summary['total_questions']}")
    print(f"  Successful responses  : {summary['successful_responses']}")
    print(f"  Errors                : {summary['error_responses']}")
    print(f"  Drill-downs used      : {summary['drill_questions_asked']}")
    print(f"  Avg confidence score  : {summary['avg_confidence_score']}")
    print(f"  Avg word count        : {summary['avg_word_count']}")
    print(f"  Confidence distribution:")
    for conf, count in summary["confidence_distribution"].items():
        print(f"    {conf}: {count}")

    # Print full readable transcript
    print_transcript(results)

    # Save JSON report (includes full answers for manual assessment)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_file = f"ai_employer_drill_test_{timestamp}.json"

    output = {
        "timestamp": timestamp,
        "persona": PERSONA,
        "summary": summary,
        "results": results,  # includes full answer text for manual review
    }

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n  Results saved: {report_file}")
    print(f"  Bring the JSON (or paste the transcript above) for manual assessment.")
    print("=" * 70)


if __name__ == "__main__":
    main()
