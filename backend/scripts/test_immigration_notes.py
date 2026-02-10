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
]

MUST_CONTAIN = [
    "IEC Working Holiday",
    "application is submitted",
    "waiting for the visa to be issued",
]

FORBIDDEN = [
    "visa is approved",
    "approved and ready to use",
]


async def run_case(case: dict) -> bool:
    req = ChatRequest(question=case["question"])
    resp = await chat(req)

    ok = True
    reasons = []

    if resp.confidence != "direct_answer":
        ok = False
        reasons.append(f"confidence={resp.confidence} (expected direct_answer)")

    answer_lower = resp.answer.lower()

    for frag in MUST_CONTAIN:
        if frag.lower() not in answer_lower:
            ok = False
            reasons.append(f"missing: {frag!r}")

    for frag in FORBIDDEN:
        if frag.lower() in answer_lower:
            ok = False
            reasons.append(f"forbidden: {frag!r}")

    print(f"{case['name']}: {'PASS' if ok else 'FAIL'}")
    print(f"  Q: {case['question']}")
    print(f"  confidence={resp.confidence}, top_score={resp.top_score:.3f}")
    print(f"  answer preview: {resp.answer[:160].replace('\\n', ' ')}")
    for r in reasons:
        print(f"  - {r}")
    print()

    return ok


async def main() -> None:
    print("Immigration / visa regression test")
    print("-" * 60)
    passed = 0

    for case in TEST_CASES:
        if await run_case(case):
            passed += 1

    print("=" * 60)
    print(f"Passed {passed}/{len(TEST_CASES)} tests")


if __name__ == "__main__":
    asyncio.run(main())


