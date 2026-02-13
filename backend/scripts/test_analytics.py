import requests
import time
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def test_chat_and_analytics():
    print_section("Analytics Feature Test")
    
    print("Step 1: Reset analytics to start fresh")
    try:
        response = requests.post(f"{API_BASE_URL}/api/analytics/reset")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reset successful: {data['message']}")
        else:
            print(f"❌ Reset failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the server is running: uvicorn app.main:app --reload")
        return
    
    print("\nStep 2: Ask some test questions")
    test_questions = [
        "What is Folio?",
        "Tell me about your experience",
        "What is Folio?",  # Duplicate to test counting
        "What programming languages do you know?",
        "What is Folio?",  # Another duplicate
        "Tell me about a challenging project",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\nAsking question {i}: '{question}'")
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/chat",
                json={"question": question},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Response received (confidence: {data.get('confidence')}, score: {data.get('top_score', 0):.4f})")
                print(f"  📝 Answer preview: {data['answer'][:80]}...")
            else:
                print(f"  ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        time.sleep(0.5)
    
    print("\n" + "-" * 80)
    print("\nStep 3: Retrieve analytics")
    try:
        response = requests.get(f"{API_BASE_URL}/api/analytics/questions")
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Analytics Summary:")
            print(f"  Total questions asked: {data['total_questions']}")
            print(f"  Unique questions: {data['total_unique']}")
            
            print(f"\n📋 Question Breakdown:")
            for i, q in enumerate(data['questions'], 1):
                print(f"\n  {i}. Question: {q['question']}")
                print(f"     Count: {q['count']}")
                print(f"     First asked: {q['first_asked']}")
                print(f"     Last asked: {q['last_asked']}")
            
            print("\n✅ Test Summary:")
            expected_total = len(test_questions)
            expected_unique = len(set(test_questions))
            
            if data['total_questions'] == expected_total:
                print(f"  ✅ Total questions match: {expected_total}")
            else:
                print(f"  ❌ Total mismatch: expected {expected_total}, got {data['total_questions']}")
            
            if data['total_unique'] == expected_unique:
                print(f"  ✅ Unique questions match: {expected_unique}")
            else:
                print(f"  ❌ Unique mismatch: expected {expected_unique}, got {data['total_unique']}")
            
            folio_question = next((q for q in data['questions'] if q['question'] == "What is Folio?"), None)
            if folio_question and folio_question['count'] == 3:
                print(f"  ✅ 'What is Folio?' asked 3 times (correct)")
            else:
                print(f"  ❌ 'What is Folio?' count incorrect")
            
        else:
            print(f"❌ Failed to retrieve analytics: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 80)
    print("\nStep 4: Test with filters")
    
    print("\nTesting 'limit=2' parameter:")
    try:
        response = requests.get(f"{API_BASE_URL}/api/analytics/questions?limit=2")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Returned {len(data['questions'])} questions (expected 2)")
            if len(data['questions']) <= 2:
                print(f"  ✅ Limit working correctly")
        else:
            print(f"  ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print("\nTesting 'days=7' parameter:")
    try:
        response = requests.get(f"{API_BASE_URL}/api/analytics/questions?days=7")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Last 7 days: {data['total_questions']} questions")
        else:
            print(f"  ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("  Test Complete!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    test_chat_and_analytics()

