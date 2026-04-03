import os
import sys
import asyncio
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

load_dotenv(ROOT / ".env")

from app.api.chat import chat, ChatRequest  # type: ignore


TEST_CASES = [
    {
        "name": "Visa status",
        "question": "What's your visa status for Canada?",
    },
    {
        "name": "Sponsorship",
        "question": "Do you need visa sponsorship to work in Canada?",
    },
    {
        "name": "Immigration plans",
        "question": "What are your immigration plans for Canada?",
    },
    {
        "name": "Already in Canada",
        "question": "Are you already in Canada?",
    },
    {
        "name": "Where based right now",
        "question": "Where are you based right now?",
    },
]

# Phrases that MUST appear in at least one answer from the above questions.
# These are checked per-question — if none of a question's answers contain
# any MUST_CONTAIN phrase, that case fails.
MUST_CONTAIN = [
    "IEC Working Holiday",  # visa program still relevant
    "issued",               # visa is issued and valid (not pending)
    "Halifax",              # currently in Halifax
    "sponsorship",          # confirms no sponsorship needed
]

# Phrases that must NEVER appear — these indicate stale pre-move content.
FORBIDDEN = [
    "waiting for the visa",
    "biometrics",
    "application is submitted",
    "from the uk",
    "start remotely",
    "visa to be issued",
    "once the visa is active",
    "once it's active",
]


async def run_case(case: dict) -> bool:
    req = ChatRequest(question=case["question"])
    resp = await chat(req)

    ok = True
    reasons = []

    answer_lower = resp.answer.lower()

    # Check for forbidden phrases
    for frag in FORBIDDEN:
        if frag.lower() in answer_lower:
            ok = False
            reasons.append(f"FORBIDDEN found: {frag!r}")

    # For the immigration/visa questions, check that key correct phrases appear
    immigration_questions = {
        "What's your visa status for Canada?",
        "Do you need visa sponsorship to work in Canada?",
        "What are your immigration plans for Canada?",
    }
    if case["question"] in immigration_questions:
        for frag in MUST_CONTAIN:
            if frag.lower() not in answer_lower:
                ok = False
                reasons.append(f"MISSING: {frag!r}")

    # Location questions should mention Halifax
    location_questions = {
        "Are you already in Canada?",
        "Where are you based right now?",
    }
    if case["question"] in location_questions:
        if "halifax" not in answer_lower and "nova scotia" not in answer_lower:
            ok = False
            reasons.append("MISSING: Halifax or Nova Scotia not mentioned for location question")

    print(f"{case['name']}: {'PASS' if ok else 'FAIL'}")
    print(f"  Q: {case['question']}")
    print(f"  confidence={resp.confidence}, top_score={resp.top_score:.3f}")
    print(f"  answer preview: {resp.answer[:200].replace(chr(10), ' ')}")
    for r in reasons:
        print(f"  - {r}")
    print()

    return ok


async def main() -> None:
    print("Immigration / visa regression test")
    print("Validates: visa issued (not pending), Halifax location, no stale UK language")
    print("-" * 60)
    passed = 0

    for case in TEST_CASES:
        if await run_case(case):
            passed += 1

    print("=" * 60)
    print(f"Passed {passed}/{len(TEST_CASES)} tests")
    if passed == len(TEST_CASES):
        print("All immigration/location assertions correct.")
    else:
        print(f"{len(TEST_CASES) - passed} test(s) failed — check output above.")


if __name__ == "__main__":
    asyncio.run(main())
