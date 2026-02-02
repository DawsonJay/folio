import sys
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library not found. Install it with: pip install requests")
    sys.exit(1)

API_URL = "http://localhost:8000/api/chat"

QUESTIONS_BY_CATEGORY = {
    "Background & Story": [
        "Tell me about yourself",
        "What's your background?",
        "Walk me through your career journey",
    ],
    "Technical Skills": [
        "What are your strongest technical skills?",
        "Walk me through your React experience",
        "What's your experience with Python and AI/ML?",
        "Tell me about your full-stack development experience",
        "What technologies are you most comfortable with?",
    ],
    "Projects": [
        "What were some of your favorite projects?",
        "Tell me about the Atlantis project",
        "Tell me about the Nexus dashboard",
        "What was the most technically challenging project you've worked on?",
        "Tell me about a project where you had to learn something new",
    ],
    "Work Experience": [
        "What's your proudest achievement at Nurtur?",
        "Tell me about your current role",
        "How do you collaborate with other teams?",
        "Why are you looking for a new role?",
    ],
    "Soft Skills": [
        "Tell me about a time you had to solve a difficult technical problem",
        "How do you approach debugging?",
        "How do you communicate technical concepts to non-technical people?",
    ],
    "Career Goals": [
        "What are your career goals?",
        "What are you looking for in your next role?",
        "Where do you see yourself in five years?",
    ],
    "Practical & Logistics": [
        "Are you open to remote work?",
        "When can you start?",
    ],
}

def get_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")

def get_readable_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def test_question(question: str, category: str, question_number: int, total: int) -> Dict[str, Any]:
    print(f"\n[{question_number}/{total}] Testing: {question}")
    print(f"    Category: {category}")
    print("-" * 80)
    
    start_time = time.time()
    result = {
        "question_number": question_number,
        "category": category,
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
            
            word_count = len(result["answer"].split())
            result["word_count"] = word_count
            
            print(f"✅ Success ({response_time_ms}ms, {word_count} words)")
            print(f"   Confidence: {result['confidence']}, Score: {result['top_score']:.4f}")
            print(f"   Emotion: {result['emotion']}")
            print(f"   Suggestions: {len(result['suggestions'])}")
        else:
            result["error"] = f"HTTP {response.status_code}: {response.text}"
            print(f"❌ Failed: {result['error']}")
            
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection error: Backend server not running"
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
    
    confidence_dist = {}
    emotion_dist = {}
    
    for r in successful:
        conf = r.get("confidence", "unknown")
        emotion = r.get("emotion", "unknown")
        confidence_dist[conf] = confidence_dist.get(conf, 0) + 1
        emotion_dist[emotion] = emotion_dist.get(emotion, 0) + 1
    
    categories_covered = len(set(r.get("category", "") for r in results))
    
    return {
        "total_questions": len(results),
        "successful_responses": len(successful),
        "failed_responses": len(failed),
        "categories_covered": categories_covered,
        "average_response_time_ms": int(avg_response_time),
        "average_word_count": int(avg_word_count),
        "confidence_distribution": confidence_dist,
        "emotion_distribution": emotion_dist,
    }

def generate_markdown_report(results: List[Dict[str, Any]], summary: Dict[str, Any], timestamp: str) -> str:
    md = []
    
    md.append("# Folio Employer-Readiness Report")
    md.append(f"\n**Generated**: {get_readable_timestamp()}")
    md.append(f"\n**API URL**: {API_URL}")
    md.append("\n---")
    
    md.append("\n## Summary")
    md.append(f"\n- **Total Questions**: {summary['total_questions']}")
    md.append(f"- **Successful Responses**: {summary['successful_responses']}")
    md.append(f"- **Failed Responses**: {summary['failed_responses']}")
    md.append(f"- **Categories Covered**: {summary['categories_covered']}")
    md.append(f"- **Average Response Time**: {summary['average_response_time_ms']}ms")
    md.append(f"- **Average Word Count**: {summary['average_word_count']} words")
    
    md.append("\n### Confidence Distribution")
    for conf, count in summary['confidence_distribution'].items():
        md.append(f"- {conf}: {count}")
    
    md.append("\n### Emotion Distribution")
    for emotion, count in summary['emotion_distribution'].items():
        md.append(f"- {emotion}: {count}")
    
    md.append("\n---\n")
    
    results_by_category = {}
    for result in results:
        category = result.get("category", "Unknown")
        if category not in results_by_category:
            results_by_category[category] = []
        results_by_category[category].append(result)
    
    for category in QUESTIONS_BY_CATEGORY.keys():
        if category not in results_by_category:
            continue
            
        md.append(f"\n## {category}\n")
        
        for result in results_by_category[category]:
            q_num = result.get("question_number", 0)
            question = result.get("question", "")
            
            md.append(f"### Q{q_num}: {question}\n")
            
            if result.get("success", False):
                md.append(f"**Confidence**: {result.get('confidence', 'unknown')} ({result.get('top_score', 0.0):.4f})")
                md.append(f"**Emotion**: {result.get('emotion', 'unknown')}")
                md.append(f"**Word Count**: {result.get('word_count', 0)}")
                md.append(f"**Response Time**: {result.get('response_time_ms', 0)}ms\n")
                
                md.append("**Answer**:")
                md.append(f"\n{result.get('answer', '')}\n")
                
                suggestions = result.get('suggestions', [])
                if suggestions:
                    md.append("**Suggestions**:")
                    for i, sugg in enumerate(suggestions, 1):
                        sugg_text = sugg.get('text', sugg) if isinstance(sugg, dict) else sugg
                        md.append(f"{i}. {sugg_text}")
                    md.append("")
                
                project_links = result.get('projectLinks')
                if project_links:
                    md.append("**Project Links**:")
                    for project_name, links in project_links.items():
                        md.append(f"- **{project_name}**:")
                        if links.get('demo'):
                            md.append(f"  - Demo: {links['demo']}")
                        if links.get('github'):
                            md.append(f"  - GitHub: {links['github']}")
                    md.append("")
                
                md.append("**Evaluation Checklist**:")
                md.append("- [ ] Professional tone")
                md.append("- [ ] Clear and concise")
                md.append("- [ ] Highlights key strengths")
                md.append("- [ ] Appropriate length (300-400 words)")
                md.append("- [ ] No markdown formatting issues")
                md.append("- [ ] Correct pronouns (I for personal, we for work)")
                md.append("- [ ] Project status indicated (ongoing/complete/cancelled)")
                md.append("- [ ] Technical terms explained for non-technical audience")
                md.append("- [ ] Suggestions are relevant and specific to James")
                md.append("- [ ] No problematic suggestions (company preferences, etc.)")
                
                md.append("\n**Your Notes**:")
                md.append("_[Add your evaluation notes here]_\n")
            else:
                md.append(f"**❌ FAILED**: {result.get('error', 'Unknown error')}\n")
            
            md.append("---\n")
    
    return "\n".join(md)

def main():
    print("=" * 80)
    print("  Comprehensive Employer-Readiness Test")
    print("=" * 80)
    
    all_questions = []
    for category, questions in QUESTIONS_BY_CATEGORY.items():
        for question in questions:
            all_questions.append((category, question))
    
    total_questions = len(all_questions)
    
    print(f"\nAPI URL: {API_URL}")
    print(f"Total Questions: {total_questions}")
    print(f"Categories: {len(QUESTIONS_BY_CATEGORY)}\n")
    
    results = []
    
    for i, (category, question) in enumerate(all_questions, 1):
        result = test_question(question, category, i, total_questions)
        results.append(result)
        
        if i < total_questions:
            time.sleep(0.5)
    
    summary = calculate_summary(results)
    
    results_dir = Path(__file__).parent.parent / "test-results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = get_timestamp()
    output_file = results_dir / f"employer-readiness-report-{timestamp}.md"
    
    markdown_content = generate_markdown_report(results, summary, timestamp)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print("\n" + "=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    print(f"\nTotal Questions: {summary['total_questions']}")
    print(f"Successful: {summary['successful_responses']}")
    print(f"Failed: {summary['failed_responses']}")
    print(f"Categories Covered: {summary['categories_covered']}")
    print(f"Average Response Time: {summary['average_response_time_ms']}ms")
    print(f"Average Word Count: {summary['average_word_count']} words")
    print(f"\nConfidence Distribution:")
    for conf, count in summary['confidence_distribution'].items():
        print(f"  {conf}: {count}")
    print(f"\nEmotion Distribution:")
    for emotion, count in summary['emotion_distribution'].items():
        print(f"  {emotion}: {count}")
    
    print(f"\n✅ Markdown report saved to: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()

