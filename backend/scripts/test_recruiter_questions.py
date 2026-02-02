import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library not found. Install it with: pip install requests")
    sys.exit(1)

API_URL = "http://localhost:8000/api/chat"

RECRUITER_QUESTIONS = [
    "Tell me about yourself",
    "What are your strongest technical skills?",
    "Why are you looking for a new role?",
    "What are you looking for in your next role?",
    "Tell me about a project you're proud of",
    "What's your experience with React?",
    "How do you approach problem-solving?",
    "What are your career goals?",
    "Why should we hire you?",
    "What's your experience with AI/ML?",
]

def get_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")

def test_question(question: str, question_number: int) -> Dict[str, Any]:
    print(f"\n[{question_number}/{len(RECRUITER_QUESTIONS)}] Testing: {question}")
    print("-" * 80)
    
    start_time = time.time()
    result = {
        "question_number": question_number,
        "question": question,
        "timestamp": get_timestamp(),
        "success": False,
        "error": None,
    }
    
    try:
        response = requests.post(
            API_URL,
            json={"question": question},
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        response_time_ms = int((time.time() - start_time) * 1000)
        result["response_time_ms"] = response_time_ms
        
        if response.status_code == 200:
            data = response.json()
            result["success"] = True
            result["answer"] = data.get("answer", "")
            result["suggestions"] = data.get("suggestions", [])
            result["emotion"] = data.get("emotion", "happy")
            result["confidence"] = data.get("confidence", "unknown")
            result["top_score"] = data.get("top_score", 0.0)
            result["projectLinks"] = data.get("projectLinks", None)
            
            print(f"✅ Success ({response_time_ms}ms)")
            print(f"   Confidence: {result['confidence']}, Score: {result['top_score']:.4f}")
            print(f"   Emotion: {result['emotion']}")
            print(f"   Suggestions: {len(result['suggestions'])}")
        else:
            result["error"] = f"HTTP {response.status_code}: {response.text}"
            print(f"❌ Failed: {result['error']}")
            
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection error: Backend server not running. Start it with 'npm run dev:backend' or 'uvicorn app.main:app --reload'"
        print(f"❌ Connection Error: Backend server not running")
    except requests.exceptions.Timeout:
        result["error"] = "Request timeout: API took too long to respond"
        print(f"❌ Timeout: API took too long to respond")
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        print(f"❌ Error: {str(e)}")
    
    return result

def calculate_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    successful = [r for r in results if r.get("success", False)]
    failed = [r for r in results if not r.get("success", False)]
    
    response_times = [r.get("response_time_ms", 0) for r in successful]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    confidence_dist = {}
    emotion_dist = {}
    
    for r in successful:
        conf = r.get("confidence", "unknown")
        emotion = r.get("emotion", "unknown")
        confidence_dist[conf] = confidence_dist.get(conf, 0) + 1
        emotion_dist[emotion] = emotion_dist.get(emotion, 0) + 1
    
    return {
        "total_questions": len(results),
        "successful_responses": len(successful),
        "failed_responses": len(failed),
        "average_response_time_ms": int(avg_response_time),
        "confidence_distribution": confidence_dist,
        "emotion_distribution": emotion_dist,
    }

def main():
    print("=" * 80)
    print("  Recruiter Questions Test")
    print("=" * 80)
    print(f"\nAPI URL: {API_URL}")
    print(f"Total Questions: {len(RECRUITER_QUESTIONS)}\n")
    
    results = []
    
    for i, question in enumerate(RECRUITER_QUESTIONS, 1):
        result = test_question(question, i)
        results.append(result)
        
        if i < len(RECRUITER_QUESTIONS):
            time.sleep(0.5)
    
    summary = calculate_summary(results)
    
    output_data = {
        "test_metadata": {
            "timestamp": get_timestamp(),
            "api_url": API_URL,
            "total_questions": len(RECRUITER_QUESTIONS),
        },
        "results": results,
        "summary": summary,
    }
    
    results_dir = Path(__file__).parent.parent / "test-results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = get_timestamp()
    output_file = results_dir / f"recruiter-questions-test-{timestamp}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    print(f"\nTotal Questions: {summary['total_questions']}")
    print(f"Successful: {summary['successful_responses']}")
    print(f"Failed: {summary['failed_responses']}")
    print(f"Average Response Time: {summary['average_response_time_ms']}ms")
    print(f"\nConfidence Distribution:")
    for conf, count in summary['confidence_distribution'].items():
        print(f"  {conf}: {count}")
    print(f"\nEmotion Distribution:")
    for emotion, count in summary['emotion_distribution'].items():
        print(f"  {emotion}: {count}")
    
    print(f"\n✅ Results saved to: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()

