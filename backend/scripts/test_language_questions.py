import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library not found. Install it with: pip install requests")
    sys.exit(1)

API_URL = "http://localhost:8000/api/chat"

LANGUAGE_QUESTIONS = [
    "What languages do you know?",
    "What programming languages are you familiar with?",
    "Tell me about the programming languages you use",
    "What languages have you worked with?",
    "What backend languages do you know?",
    "Do you know C#?",
    "Do you know Java?",
    "What's your experience with Python?",
    "What languages did you use at Nurtur?",
]

def get_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")

def test_question(question: str, question_number: int) -> Dict[str, Any]:
    print(f"\n[{question_number}/{len(LANGUAGE_QUESTIONS)}] Testing: {question}")
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
            answer = data.get("answer", "")
            result["answer"] = answer
            result["word_count"] = len(answer.split())
            result["character_count"] = len(answer)
            result["suggestions"] = data.get("suggestions", [])
            result["emotion"] = data.get("emotion", "happy")
            result["confidence"] = data.get("confidence", "unknown")
            result["top_score"] = data.get("top_score", 0.0)
            
            languages_mentioned = []
            language_keywords = {
                "typescript": ["typescript", "ts", "type script"],
                "javascript": ["javascript", "js", "java script"],
                "c#": ["c#", "c sharp", "csharp"],
                "java": ["java"],
                "python": ["python"],
                "lua": ["lua"],
                "react": ["react"],
            }
            
            answer_lower = answer.lower()
            for lang, keywords in language_keywords.items():
                if any(keyword in answer_lower for keyword in keywords):
                    languages_mentioned.append(lang)
            
            result["languages_mentioned"] = languages_mentioned
            result["mentions_csharp"] = "c#" in languages_mentioned
            result["mentions_java"] = "java" in languages_mentioned
            result["mentions_python"] = "python" in languages_mentioned
            result["mentions_lua"] = "lua" in languages_mentioned
            result["mentions_typescript"] = "typescript" in languages_mentioned
            
            print(f"✅ Success ({response_time_ms}ms)")
            print(f"   Confidence: {result['confidence']}, Score: {result['top_score']:.4f}")
            print(f"   Word Count: {result['word_count']}")
            print(f"   Character Count: {result['character_count']}")
            print(f"   Languages Mentioned: {', '.join(languages_mentioned) if languages_mentioned else 'None'}")
            
            if result['word_count'] < 100:
                print(f"   ⚠️  WARNING: Response is quite short ({result['word_count']} words, expected 150-400)")
            elif result['word_count'] < 150:
                print(f"   ⚠️  WARNING: Response is below minimum recommended length ({result['word_count']} words, expected 150-400)")
            
            print(f"\n   Answer Preview (first 300 chars):")
            preview = answer[:300] + "..." if len(answer) > 300 else answer
            print(f"   {preview}")
            
        else:
            result["error"] = f"HTTP {response.status_code}: {response.text}"
            print(f"❌ Failed: {result['error']}")
            
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection error: Backend server not running. Start it with 'uvicorn app.main:app --reload'"
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
    
    word_counts = [r.get("word_count", 0) for r in successful]
    avg_word_count = sum(word_counts) / len(word_counts) if word_counts else 0
    min_word_count = min(word_counts) if word_counts else 0
    max_word_count = max(word_counts) if word_counts else 0
    
    short_responses = [r for r in successful if r.get("word_count", 0) < 150]
    
    confidence_dist = {}
    emotion_dist = {}
    language_mentions = {
        "typescript": 0,
        "javascript": 0,
        "c#": 0,
        "java": 0,
        "python": 0,
        "lua": 0,
    }
    
    for r in successful:
        conf = r.get("confidence", "unknown")
        emotion = r.get("emotion", "unknown")
        confidence_dist[conf] = confidence_dist.get(conf, 0) + 1
        emotion_dist[emotion] = emotion_dist.get(emotion, 0) + 1
        
        for lang in language_mentions.keys():
            if r.get(f"mentions_{lang.replace('#', 'sharp')}", False):
                language_mentions[lang] += 1
    
    return {
        "total_questions": len(results),
        "successful_responses": len(successful),
        "failed_responses": len(failed),
        "average_response_time_ms": int(avg_response_time),
        "word_count_stats": {
            "average": int(avg_word_count),
            "minimum": min_word_count,
            "maximum": max_word_count,
        },
        "short_responses_count": len(short_responses),
        "short_responses": [{"question": r["question"], "word_count": r.get("word_count", 0)} for r in short_responses],
        "confidence_distribution": confidence_dist,
        "emotion_distribution": emotion_dist,
        "language_mentions": language_mentions,
    }

def main():
    print("=" * 80)
    print("  Programming Languages Questions Test")
    print("=" * 80)
    print(f"\nAPI URL: {API_URL}")
    print(f"Total Questions: {len(LANGUAGE_QUESTIONS)}\n")
    print("Testing questions about:")
    print("  - Programming languages familiarity")
    print("  - Language experience and usage")
    print("  - Specific language knowledge (C#, Java, Python, etc.)")
    print("\nExpected response length: 150-400 words")
    print("=" * 80)
    
    results = []
    
    for i, question in enumerate(LANGUAGE_QUESTIONS, 1):
        result = test_question(question, i)
        results.append(result)
        
        if i < len(LANGUAGE_QUESTIONS):
            time.sleep(0.5)
    
    summary = calculate_summary(results)
    
    output_data = {
        "test_metadata": {
            "timestamp": get_timestamp(),
            "api_url": API_URL,
            "total_questions": len(LANGUAGE_QUESTIONS),
            "test_focus": "Programming languages questions and response length",
        },
        "results": results,
        "summary": summary,
    }
    
    results_dir = Path(__file__).parent.parent / "test-results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = get_timestamp()
    output_file = results_dir / f"language-questions-test-{timestamp}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    print(f"\nTotal Questions: {summary['total_questions']}")
    print(f"Successful: {summary['successful_responses']}")
    print(f"Failed: {summary['failed_responses']}")
    print(f"Average Response Time: {summary['average_response_time_ms']}ms")
    
    print(f"\n📊 Word Count Statistics:")
    print(f"   Average: {summary['word_count_stats']['average']} words")
    print(f"   Minimum: {summary['word_count_stats']['minimum']} words")
    print(f"   Maximum: {summary['word_count_stats']['maximum']} words")
    print(f"   Expected Range: 150-400 words")
    
    if summary['short_responses_count'] > 0:
        print(f"\n⚠️  Short Responses (< 150 words): {summary['short_responses_count']}")
        for sr in summary['short_responses']:
            print(f"   - '{sr['question']}': {sr['word_count']} words")
    else:
        print(f"\n✅ All responses meet minimum length requirement (150 words)")
    
    print(f"\n📊 Language Mentions:")
    for lang, count in summary['language_mentions'].items():
        if count > 0:
            print(f"   {lang}: {count}/{summary['successful_responses']} responses")
    
    print(f"\n📊 Confidence Distribution:")
    for conf, count in summary['confidence_distribution'].items():
        print(f"   {conf}: {count}")
    
    print(f"\n📊 Emotion Distribution:")
    for emotion, count in summary['emotion_distribution'].items():
        print(f"   {emotion}: {count}")
    
    print(f"\n📄 Full results saved to: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()

