import requests

API_URL = "http://localhost:8000/api/chat"

questions = [
    "Are you okay with hybrid work - 2 days in office?",
    "Are you comfortable with hybrid work?",
    "Can you work in the office 2 days a week?",
]

for q in questions:
    response = requests.post(API_URL, json={"question": q, "session_id": "test-hybrid"})
    data = response.json()
    
    print(f"\nQ: {q}")
    print(f"Confidence: {data.get('confidence')}")
    print(f"Score: {data.get('top_score', 0):.3f}")
    print(f"Answer: {data.get('answer', '')[:200]}...")
