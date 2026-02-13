"""
Comprehensive Direct Answer Quality Test

Validates that tier-1 direct answers are high quality and frame the candidate
well to recruiters. Tests retrieval (right answer found) and content (gold standard).

Run: python test_direct_answer_quality.py
Requires: Backend API running at http://localhost:8000
"""

import re
import json
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    raise

API_URL = "http://localhost:8000/api/chat"
DIRECT_ANSWER_THRESHOLD = 0.65

# Questions by category (aligned with DIRECT-ANSWER-TEST-SPEC.md)
QUESTIONS_BY_CATEGORY = {
    "opening": [
        "Tell me about yourself",
        "Walk me through your experience with React and TypeScript",
        "Why are you looking for a new role?",
        "Why should we hire you?",
    ],
    "work_experience": [
        "Tell me about your role at Nurtur",
        "What was your biggest accomplishment at Nurtur?",
        "What was your biggest accomplishment there?",
        "Have you led any projects?",
        "How did you grow in your position at Nurtur?",
        "Tell me about your most recent role",
        "What did you do at Nurtur?",
    ],
    "technical": [
        "What's your experience with state management? Redux, Context?",
        "Tell me about a complex technical problem you've solved",
        "How do you approach performance optimization?",
        "What's your testing strategy?",
        "How do you make technical decisions?",
        "What's your debugging process?",
    ],
    "team": [
        "What size team do you prefer?",
        "Tell me about a time you mentored someone",
        "How do you handle code reviews?",
        "How did you work with backend developers?",
        "How do you handle conflict in teams?",
    ],
    "ai_ml": [
        "I see you have AI/ML experience - tell me about that",
        "Have you integrated AI into web applications?",
        "What AI/ML experience do you have?",
    ],
    "logistics": [
        "What's your visa status for Canada?",
        "When can you start?",
        "Are you okay with hybrid work - 2 days in office?",
        "Are you comfortable with hybrid work?",
        "Are you open to remote work?",
        "What are your salary expectations?",
        "What's your current employment status?",
    ],
    "canada": [
        "Why are you looking to move to Canada?",
        "Why Canada?",
        "How will you handle the transition period to Canada?",
    ],
    "behavioral": [
        "What are your strengths?",
        "What's your biggest weakness?",
        "How do you handle failure?",
        "Tell me about a mistake you made",
        "What are you looking for in your next role?",
    ],
    "edge": [
        "What project are you most proud of?",
        "What's your favorite project?",
        "Which project best demonstrates your skills?",
    ],
}

# Critical questions that MUST return direct answers
CRITICAL_QUESTIONS = {
    "Tell me about yourself",
    "Why should we hire you?",
    "What are your salary expectations?",
    "When can you start?",
    "Are you okay with hybrid work - 2 days in office?",
    "Are you comfortable with hybrid work?",
    "Are you open to remote work?",
    "What was your biggest accomplishment at Nurtur?",
    "What was your biggest accomplishment there?",
    "What's your current employment status?",
}

# Prescriptive phrases (red flags)
PRESCRIPTIVE_PATTERNS = [
    r"\bthis demonstrates\b",
    r"\bthis proves\b",
    r"\bthis shows\b",
    r"\bmy superpower is\b",
    r"\bthe proof is in\b",
    r"\bwhat makes me unique is\b",
    r"\bwhat sets me apart\b",
    r"\bwhat makes me different is\b",
]

# Negative / defensive openings
NEGATIVE_OPENINGS = [
    "the question is a little vague",
    "the question is vague",
    "i'm better with more specific questions",
    "i am currently unemployed",  # as opener for non-status questions
]

# Integrations overclaim
INTEGRATIONS_OVERCLAIM = re.compile(
    r"\bsolo\b.*\bintegrations\b|\bintegrations\b.*\bsolo\b",
    re.IGNORECASE,
)


def ask_api(question: str, session_id: str) -> dict:
    """Call chat API and return answer, confidence, score."""
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
            "answer": f"ERROR: {str(e)}",
            "confidence": "error",
            "score": 0.0,
        }


def word_count(text: str) -> int:
    return len(text.split())


def check_red_flags(question: str, answer: str) -> list[str]:
    """Return list of red flags found in the answer."""
    flags = []
    a = answer.lower()
    first_sentence = (answer.split(".")[0] or "").lower()[:120]

    # Junior (avoid in isolation; "from junior to" is ok)
    if "junior" in a:
        if "junior developer" in a or "junior frontend" in a or "as a junior" in a:
            flags.append("Mentions junior role/title")
    # Prescriptive language
    for pat in PRESCRIPTIVE_PATTERNS:
        if re.search(pat, a):
            flags.append("Prescriptive language (tell reader what to think)")
            break
    # Negative / defensive opening
    for neg in NEGATIVE_OPENINGS:
        if neg in first_sentence:
            flags.append("Defensive or negative opening")
            break
    # Integrations overclaim
    if INTEGRATIONS_OVERCLAIM.search(answer):
        flags.append("Integrations framed as solo (should be sole frontend + backend mentorship)")
    # Negative environment language
    if "ego" in a or "pretension" in a:
        flags.append("Negative language about environment")
    # Salary dodge
    if "salary" in question.lower() or "salary expectations" in question.lower():
        if "£" not in answer and "gbp" not in a and ("$" not in answer or "research" in a and "55" not in answer and "75" not in answer):
            # Allow £55-75K or similar
            if not re.search(r"55\s*[-–]\s*75|55k|75k|55,?000|75,?000", a):
                flags.append("Salary question answered without clear range/number")
    # Too long
    wc = word_count(answer)
    if wc > 350:
        flags.append(f"Too long ({wc} words, loses attention)")
    # Too short and generic
    if wc < 60 and ("integrations" not in a and "nexus" not in a and "nurtur" not in a and "react" not in a):
        flags.append("Very short answer with no concrete anchors")

    return flags


def check_positive_signals(answer: str) -> list[str]:
    """Return list of positive signals."""
    signals = []
    a = answer.lower()
    if "3+ years" in answer or "zero maintenance" in a:
        signals.append("Credibility anchor (3+ years / zero maintenance)")
    if "integrations dashboard" in a or "integrations" in a:
        signals.append("Integrations Dashboard mentioned")
    if "nexus" in a:
        signals.append("Nexus mentioned")
    if "technical lead" in a and "nexus" in a:
        signals.append("Nexus framed as technical lead")
    if "sole frontend" in a or "learned backend" in a or "backend mentorship" in a:
        signals.append("Integrations framed correctly (frontend ownership / mentorship)")
    if "mentored" in a or "mentoring" in a:
        signals.append("Mentoring experience")
    if re.search(r"\d+\+?\s*(seconds?|years?|users?|developers?)", a):
        signals.append("Concrete metrics")
    if answer.strip().lower().startswith(("yes", "absolutely", "my entire", "i've", "i ")):
        signals.append("Direct opening (no hedging)")
    return signals


def length_ok(question: str, word_count: int) -> tuple[bool, str]:
    """True if length in acceptable range; else (False, reason)."""
    if word_count < 80 and word_count > 0:
        return False, f"Short ({word_count} words)"
    if word_count > 300:
        return False, f"Long ({word_count} words)"
    return True, "OK"


def run_test(session_id: str) -> list[dict]:
    """Run full test; return list of result dicts."""
    results = []
    all_questions = []
    for cat, qs in QUESTIONS_BY_CATEGORY.items():
        for q in qs:
            all_questions.append((cat, q))

    for i, (category, question) in enumerate(all_questions, 1):
        api = ask_api(question, session_id)
        answer = api["answer"]
        confidence = api["confidence"]
        score = api["score"]
        wc = word_count(answer)

        used_direct = confidence == "direct_answer" and score >= DIRECT_ANSWER_THRESHOLD
        red_flags = check_red_flags(question, answer)
        positive = check_positive_signals(answer)
        length_ok_flag, length_note = length_ok(question, wc)

        is_critical = question in CRITICAL_QUESTIONS
        critical_pass = True
        if is_critical:
            if not used_direct:
                critical_pass = False
                if not red_flags:
                    red_flags = ["Critical question did not use direct answer (score={:.2f})".format(score)]
            if red_flags:
                critical_pass = False

        pass_fail = "PASS" if not red_flags and (not is_critical or critical_pass) else "FAIL"

        results.append({
            "category": category,
            "question": question,
            "answer_preview": (answer[:200] + "..." if len(answer) > 200 else answer),
            "word_count": wc,
            "confidence": confidence,
            "score": round(score, 3),
            "used_direct_answer": used_direct,
            "is_critical": is_critical,
            "critical_pass": critical_pass if is_critical else None,
            "red_flags": red_flags,
            "positive_signals": positive,
            "length_ok": length_ok_flag,
            "length_note": length_note,
            "pass_fail": pass_fail,
        })
        time.sleep(0.3)

    return results


def summarize(results: list[dict]) -> dict:
    total = len(results)
    direct_count = sum(1 for r in results if r["used_direct_answer"])
    critical = [r for r in results if r["is_critical"]]
    critical_pass = sum(1 for r in critical if r["critical_pass"])
    critical_fail = len(critical) - critical_pass
    total_red = sum(len(r["red_flags"]) for r in results)
    fails = [r for r in results if r["pass_fail"] == "FAIL"]

    # Grade: critical pass is most important; then red flag count
    if critical_fail > 0:
        grade = "F" if critical_fail >= 2 else "C"
    elif total_red == 0:
        grade = "A"
    elif total_red <= 3:
        grade = "A"
    elif total_red <= 6:
        grade = "B"
    elif total_red <= 10:
        grade = "C"
    else:
        grade = "F"

    return {
        "total_questions": total,
        "direct_answer_count": direct_count,
        "direct_answer_rate_pct": round(100 * direct_count / total, 1) if total else 0,
        "critical_total": len(critical),
        "critical_pass": critical_pass,
        "critical_fail": critical_fail,
        "total_red_flags": total_red,
        "fail_count": len(fails),
        "grade": grade,
        "failed_questions": [r["question"] for r in fails],
    }


def red_flag_breakdown(results: list[dict]) -> dict[str, int]:
    """Count red flags by type for prioritization."""
    breakdown = {}
    for r in results:
        for flag in r["red_flags"]:
            # Normalize: take first 40 chars as key for "Too long (359 words...)" etc
            key = flag.split("(")[0].strip() if "(" in flag else flag
            breakdown[key] = breakdown.get(key, 0) + 1
    return breakdown


def write_report(results: list[dict], summary: dict, out_path: str) -> None:
    breakdown = red_flag_breakdown(results)
    lines = [
        "# Direct Answer Quality Report",
        "",
        "Generated: " + datetime.now().isoformat(),
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total questions | {summary['total_questions']} |",
        f"| Direct answer rate | {summary['direct_answer_rate_pct']}% |",
        f"| Critical questions pass | {summary['critical_pass']}/{summary['critical_total']} |",
        f"| Total red flags | {summary['total_red_flags']} |",
        f"| Questions failed | {summary['fail_count']} |",
        f"| **Grade** | **{summary['grade']}** |",
        "",
    ]
    if breakdown:
        lines.append("### Red flags by type (prioritize fixes)")
        for flag_type, count in sorted(breakdown.items(), key=lambda x: -x[1]):
            lines.append(f"- **{flag_type}**: {count}")
        lines.append("")
    lines.extend([
        "## Failed or Flagged Questions",
        "",
    ])
    for r in results:
        if r["pass_fail"] != "PASS" or r["red_flags"]:
            lines.append(f"### {r['question']}")
            lines.append(f"- Category: {r['category']}")
            lines.append(f"- Confidence: {r['confidence']} | Score: {r['score']} | Words: {r['word_count']}")
            lines.append(f"- Direct answer used: {r['used_direct_answer']}")
            if r["red_flags"]:
                lines.append("- Red flags:")
                for f in r["red_flags"]:
                    lines.append(f"  - {f}")
            if r["positive_signals"]:
                lines.append("- Positive signals: " + ", ".join(r["positive_signals"]))
            lines.append("")
    if summary["failed_questions"]:
        lines.append("## All Failed Questions (list)")
        for q in summary["failed_questions"]:
            lines.append(f"- {q}")
    Path(out_path).write_text("\n".join(lines), encoding="utf-8")


def main():
    print("Direct Answer Quality Test")
    print("=" * 60)
    session_id = f"quality-test-{int(time.time())}"
    results = run_test(session_id)
    summary = summarize(results)

    print(f"\nTotal questions: {summary['total_questions']}")
    print(f"Direct answer rate: {summary['direct_answer_rate_pct']}%")
    print(f"Critical pass: {summary['critical_pass']}/{summary['critical_total']}")
    print(f"Total red flags: {summary['total_red_flags']}")
    print(f"Grade: {summary['grade']}")

    if summary["fail_count"] > 0:
        print(f"\nFailed questions ({summary['fail_count']}):")
        for q in summary["failed_questions"][:15]:
            print(f"  - {q}")
        if len(summary["failed_questions"]) > 15:
            print(f"  ... and {len(summary['failed_questions']) - 15} more")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = f"direct-answer-quality-{timestamp}.json"
    report_path = f"direct-answer-quality-report-{timestamp}.md"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "results": results}, f, indent=2)
    write_report(results, summary, report_path)
    print(f"\nResults: {json_path}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
