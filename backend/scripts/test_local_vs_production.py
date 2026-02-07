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

LOCAL_API_URL = "http://localhost:8000/api/chat"
PRODUCTION_API_URL = "https://folio-production-16b7.up.railway.app/api/chat"

TEST_QUESTIONS = [
    "What is your experience?",
    "Tell me about yourself",
    "What is your current employment status?",
    "Where do you work?",
    "What do you do?",
]

PRESENT_TENSE_INDICATORS = [
    "currently",
    "i am",
    "i'm",
    "i work",
    "i'm working",
    "i'm focused",
    "right now",
    "at nurtur.*is",
    "at nurtur.*allows",
    "at nurtur.*involves",
]

PAST_TENSE_INDICATORS = [
    "worked at nurtur",
    "was made redundant",
    "i was",
    "i worked",
    "i built",
    "i contributed",
    "july 2022 - february 2026",
    "3.5 years",
    "three and a half years",
]

def get_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")

def test_endpoint(api_url: str, question: str, environment: str) -> Dict[str, Any]:
    result = {
        "environment": environment,
        "api_url": api_url,
        "question": question,
        "success": False,
        "error": None,
        "answer": "",
        "present_tense_found": [],
        "past_tense_found": [],
        "has_issue": False,
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            api_url,
            json={"question": question},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response_time_ms = int((time.time() - start_time) * 1000)
        result["response_time_ms"] = response_time_ms
        
        if response.status_code == 200:
            data = response.json()
            result["success"] = True
            answer = data.get("answer", "").lower()
            result["answer"] = data.get("answer", "")
            result["confidence"] = data.get("confidence", "unknown")
            result["top_score"] = data.get("top_score", 0.0)
            
            for indicator in PRESENT_TENSE_INDICATORS:
                if indicator in answer:
                    result["present_tense_found"].append(indicator)
            
            for indicator in PAST_TENSE_INDICATORS:
                if indicator in answer:
                    result["past_tense_found"].append(indicator)
            
            if result["present_tense_found"] and not result["past_tense_found"]:
                result["has_issue"] = True
            elif "currently" in answer or ("i am" in answer and "nurtur" in answer):
                result["has_issue"] = True
        else:
            result["error"] = f"HTTP {response.status_code}: {response.text[:200]}"
            
    except requests.exceptions.ConnectionError:
        result["error"] = f"Connection error: {environment} server not reachable"
    except requests.exceptions.Timeout:
        result["error"] = f"Request timeout: {environment} API took too long to respond"
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
    
    return result

def analyze_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    local_results = [r for r in results if r["environment"] == "local"]
    production_results = [r for r in results if r["environment"] == "production"]
    
    local_issues = [r for r in local_results if r.get("has_issue", False) and r.get("success", False)]
    production_issues = [r for r in production_results if r.get("has_issue", False) and r.get("success", False)]
    
    local_successful = [r for r in local_results if r.get("success", False)]
    production_successful = [r for r in production_results if r.get("success", False)]
    
    return {
        "local": {
            "total_tests": len(local_results),
            "successful": len(local_successful),
            "failed": len(local_results) - len(local_successful),
            "issues_found": len(local_issues),
            "issue_questions": [r["question"] for r in local_issues],
        },
        "production": {
            "total_tests": len(production_results),
            "successful": len(production_successful),
            "failed": len(production_results) - len(production_successful),
            "issues_found": len(production_issues),
            "issue_questions": [r["question"] for r in production_issues],
        },
    }

def main():
    print("=" * 80)
    print("  Local vs Production Employment Status Test")
    print("=" * 80)
    print(f"\nLocal API: {LOCAL_API_URL}")
    print(f"Production API: {PRODUCTION_API_URL}")
    print(f"Test Questions: {len(TEST_QUESTIONS)}")
    print("\nTesting for:")
    print("  ❌ Present tense: 'currently', 'I am at Nurtur', 'I work at Nurtur'")
    print("  ✅ Past tense: 'worked at Nurtur', 'was made redundant', '3.5 years'")
    print("\n" + "=" * 80)
    
    results = []
    
    for question in TEST_QUESTIONS:
        print(f"\n📝 Testing: '{question}'")
        print("-" * 80)
        
        local_result = test_endpoint(LOCAL_API_URL, question, "local")
        results.append(local_result)
        
        if local_result["success"]:
            status = "❌ ISSUE" if local_result["has_issue"] else "✅ OK"
            print(f"  Local: {status}")
            if local_result["present_tense_found"]:
                print(f"    Found present tense: {local_result['present_tense_found']}")
            if local_result["past_tense_found"]:
                print(f"    Found past tense: {local_result['past_tense_found']}")
            if local_result["has_issue"]:
                preview = local_result["answer"][:150] + "..." if len(local_result["answer"]) > 150 else local_result["answer"]
                print(f"    Answer preview: {preview}")
        else:
            print(f"  Local: ❌ FAILED - {local_result['error']}")
        
        time.sleep(0.5)
        
        production_result = test_endpoint(PRODUCTION_API_URL, question, "production")
        results.append(production_result)
        
        if production_result["success"]:
            status = "❌ ISSUE" if production_result["has_issue"] else "✅ OK"
            print(f"  Production: {status}")
            if production_result["present_tense_found"]:
                print(f"    Found present tense: {production_result['present_tense_found']}")
            if production_result["past_tense_found"]:
                print(f"    Found past tense: {production_result['past_tense_found']}")
            if production_result["has_issue"]:
                preview = production_result["answer"][:150] + "..." if len(production_result["answer"]) > 150 else production_result["answer"]
                print(f"    Answer preview: {preview}")
        else:
            print(f"  Production: ❌ FAILED - {production_result['error']}")
        
        time.sleep(0.5)
    
    analysis = analyze_results(results)
    
    output_data = {
        "test_metadata": {
            "timestamp": get_timestamp(),
            "local_api_url": LOCAL_API_URL,
            "production_api_url": PRODUCTION_API_URL,
            "total_questions": len(TEST_QUESTIONS),
        },
        "results": results,
        "analysis": analysis,
    }
    
    results_dir = Path(__file__).parent.parent / "test-results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = get_timestamp()
    output_file = results_dir / f"local-vs-production-test-{timestamp}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    
    print(f"\n📊 Local Environment:")
    print(f"   Total Tests: {analysis['local']['total_tests']}")
    print(f"   Successful: {analysis['local']['successful']}")
    print(f"   Failed: {analysis['local']['failed']}")
    print(f"   Issues Found: {analysis['local']['issues_found']}")
    if analysis['local']['issue_questions']:
        print(f"   ❌ Questions with issues:")
        for q in analysis['local']['issue_questions']:
            print(f"      - {q}")
    
    print(f"\n📊 Production Environment:")
    print(f"   Total Tests: {analysis['production']['total_tests']}")
    print(f"   Successful: {analysis['production']['successful']}")
    print(f"   Failed: {analysis['production']['failed']}")
    print(f"   Issues Found: {analysis['production']['issues_found']}")
    if analysis['production']['issue_questions']:
        print(f"   ❌ Questions with issues:")
        for q in analysis['production']['issue_questions']:
            print(f"      - {q}")
    
    print("\n" + "=" * 80)
    print("  DIAGNOSIS")
    print("=" * 80)
    
    local_has_issues = analysis['local']['issues_found'] > 0
    production_has_issues = analysis['production']['issues_found'] > 0
    
    if local_has_issues and production_has_issues:
        print("\n⚠️  BOTH environments have issues!")
        print("   → Problem is likely in the source notes/embeddings")
        print("   → Check that all notes have been updated to past tense")
        print("   → Regenerate embeddings: python scripts/embed_notes.py")
    elif local_has_issues and not production_has_issues:
        print("\n⚠️  Only LOCAL has issues!")
        print("   → Local embeddings may be outdated")
        print("   → Regenerate local embeddings: python scripts/embed_notes.py")
    elif not local_has_issues and production_has_issues:
        print("\n⚠️  Only PRODUCTION has issues!")
        print("   → Production deployment has old embeddings")
        print("   → Commit and push updated embeddings.json")
        print("   → Redeploy to Railway")
    else:
        print("\n✅ Both environments are correct!")
        print("   → No present-tense employment references found")
    
    print(f"\n📄 Full results saved to: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()

