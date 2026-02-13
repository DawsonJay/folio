"""
Direct test of analytics without needing OpenAI API
Tests the database and analytics service directly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.services.analytics_service import AnalyticsService
from datetime import datetime, timezone

def test_analytics_direct():
    print("\n" + "=" * 80)
    print("  Direct Analytics Test (No OpenAI Required)")
    print("=" * 80 + "\n")
    
    db = SessionLocal()
    analytics_service = AnalyticsService()
    
    print("Step 1: Reset analytics")
    count = analytics_service.reset_questions(db)
    print(f"✅ Deleted {count} existing records\n")
    
    print("Step 2: Log test questions")
    test_data = [
        ("What is Folio?", "session1", "high", 0.85, 250),
        ("Tell me about your experience", "session1", "medium", 0.55, 300),
        ("What is Folio?", "session2", "high", 0.90, 200),  # Duplicate
        ("What programming languages do you know?", "session2", "high", 0.75, 275),
        ("What is Folio?", "session3", "high", 0.88, 225),  # Another duplicate
        ("Tell me about a challenging project", "session3", "medium", 0.60, 350),
    ]
    
    for i, (question, session_id, confidence, score, response_time) in enumerate(test_data, 1):
        analytics_service.log_question(
            db=db,
            question=question,
            session_id=session_id,
            confidence=confidence,
            top_score=score,
            response_time_ms=response_time,
            answer=f"Test answer {i}"
        )
        print(f"  ✅ Logged question {i}: '{question}'")
    
    print("\n" + "-" * 80)
    print("\nStep 3: Retrieve and verify analytics\n")
    
    results = analytics_service.get_question_counts(db)
    total = analytics_service.get_total_questions(db)
    
    print(f"📊 Analytics Summary:")
    print(f"  Total questions asked: {total}")
    print(f"  Unique questions: {len(results)}")
    
    print(f"\n📋 Question Breakdown:")
    for i, result in enumerate(results, 1):
        print(f"\n  {i}. Question: {result['question']}")
        print(f"     Count: {result['count']}")
        print(f"     First asked: {result['first_asked']}")
        print(f"     Last asked: {result['last_asked']}")
    
    print("\n" + "=" * 80)
    print("  Verification")
    print("=" * 80 + "\n")
    
    expected_total = len(test_data)
    expected_unique = len(set(q[0] for q in test_data))
    
    all_passed = True
    
    if total == expected_total:
        print(f"✅ Total questions: {total} (expected {expected_total})")
    else:
        print(f"❌ Total mismatch: got {total}, expected {expected_total}")
        all_passed = False
    
    if len(results) == expected_unique:
        print(f"✅ Unique questions: {len(results)} (expected {expected_unique})")
    else:
        print(f"❌ Unique mismatch: got {len(results)}, expected {expected_unique}")
        all_passed = False
    
    folio_result = next((r for r in results if r['question'] == "What is Folio?"), None)
    if folio_result and folio_result['count'] == 3:
        print(f"✅ 'What is Folio?' asked 3 times (correct)")
    else:
        count = folio_result['count'] if folio_result else 0
        print(f"❌ 'What is Folio?' count: {count} (expected 3)")
        all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("  🎉 ALL TESTS PASSED!")
    else:
        print("  ❌ SOME TESTS FAILED")
    print("=" * 80 + "\n")
    
    db.close()
    return all_passed

if __name__ == "__main__":
    success = test_analytics_direct()
    sys.exit(0 if success else 1)

