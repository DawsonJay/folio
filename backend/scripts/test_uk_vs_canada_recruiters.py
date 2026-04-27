import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Tuple, Optional
import re

sys.path.append(str(Path(__file__).parent.parent))

load_dotenv(Path(__file__).parent.parent / ".env")

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage
from app.services.direct_answer_service import DirectAnswerService

DIRECT_ANSWER_THRESHOLD = 0.75

UK_RECRUITER_QUESTIONS = [
    "Why are you looking for a new role?",
    "What are you looking for in your next role?",
    "Tell me about yourself",
    "What's your professional background?",
    "What's your story?",
    "Where do you see yourself in five years?",
    "What are your career goals?",
    "Walk me through your career journey",
    "Tell me about your current role",
    "Tell me about your current experience",
    "What's your background?",
    "What's your availability?",
    "When can you start?",
    "What's your current employment status?",
    "Are you open to remote work?",
    "Are you willing to relocate?",
    "Why did you leave your last job?",
    "Tell me about your educational background",
]

CANADIAN_RECRUITER_QUESTIONS = [
    "Why do you want to move to Canada?",
    "Why Canada?",
    "What's your visa status?",
    "What are your immigration plans?",
    "When are you planning to move to Canada?",
    "What's your timeline for moving?",
    "Do you have a work permit for Canada?",
    "Do you need visa sponsorship?",
    "Are you planning to stay in Canada long-term?",
    "How committed are you to this move?",
]

CANADA_KEYWORDS = [
    r'\bcanada\b',
    r'\bcanadian\b',
    r'\bimmigration\b',
    r'\bvisa\b',
    r'\bworking holiday\b',
    r'\bpermanent residency\b',
    r'\bpermanent residence\b',
    r'\bmove to canada\b',
    r'\brelocat.*canada\b',
    r'\bcanada.*work\b',
]

IMMIGRATION_KEYWORDS = [
    r'\bimmigration\b',
    r'\bvisa\b',
    r'\bworking holiday\b',
    r'\bpermanent residency\b',
    r'\bpermanent residence\b',
    r'\bwork permit\b',
    r'\bvisa sponsorship\b',
    r'\bcanadian experience class\b',
]

def check_for_keywords(text: str, keywords: List[str]) -> List[str]:
    """Check if text contains any of the given keywords (case-insensitive)."""
    found = []
    text_lower = text.lower()
    for keyword in keywords:
        pattern = re.compile(keyword, re.IGNORECASE)
        if pattern.search(text_lower):
            found.append(keyword)
    return found

def get_direct_answer_response(
    question: str,
    openai_service: OpenAIService,
    direct_answer_storage: LocalEmbeddingStorage,
    direct_answer_service: DirectAnswerService
) -> Optional[Dict]:
    """Get direct answer response for a question."""
    query_embedding = openai_service.get_embedding(question)
    
    try:
        direct_answer_results = direct_answer_storage.query_similar(query_embedding, top_k=1)
        
        if direct_answer_results and direct_answer_results[0]['score'] >= DIRECT_ANSWER_THRESHOLD:
            file_path = direct_answer_results[0]['metadata']['file_path']
            direct_answer = direct_answer_service.load_direct_answer(file_path)
            return {
                "answer": direct_answer.get("answer", ""),
                "suggestions": direct_answer.get("suggestions", []),
                "score": direct_answer_results[0]['score'],
                "file_path": file_path
            }
    except Exception as e:
        print(f"Error getting direct answer for '{question}': {e}")
    
    return None

def test_uk_recruiter_questions(
    openai_service: OpenAIService,
    direct_answer_storage: LocalEmbeddingStorage,
    direct_answer_service: DirectAnswerService
) -> Dict:
    """Test that UK recruiter questions don't mention Canada/immigration."""
    results = {
        "passed": [],
        "failed": [],
        "details": []
    }
    
    print("\n" + "="*80)
    print("TESTING UK RECRUITER QUESTIONS")
    print("="*80)
    print("These questions should NOT mention Canada or immigration.\n")
    
    for question in UK_RECRUITER_QUESTIONS:
        response = get_direct_answer_response(
            question, openai_service, direct_answer_storage, direct_answer_service
        )
        
        if not response:
            results["failed"].append(question)
            results["details"].append({
                "question": question,
                "status": "FAILED",
                "reason": "No direct answer found"
            })
            continue
        
        answer = response["answer"]
        suggestions = response["suggestions"]
        
        canada_keywords_found = check_for_keywords(answer, CANADA_KEYWORDS)
        immigration_keywords_found = check_for_keywords(answer, IMMIGRATION_KEYWORDS)
        
        suggestion_issues = []
        for suggestion in suggestions:
            suggestion_canada = check_for_keywords(suggestion, CANADA_KEYWORDS)
            suggestion_immigration = check_for_keywords(suggestion, IMMIGRATION_KEYWORDS)
            if suggestion_canada or suggestion_immigration:
                suggestion_issues.append({
                    "suggestion": suggestion,
                    "canada_keywords": suggestion_canada,
                    "immigration_keywords": suggestion_immigration
                })
        
        if canada_keywords_found or immigration_keywords_found or suggestion_issues:
            results["failed"].append(question)
            results["details"].append({
                "question": question,
                "status": "FAILED",
                "answer_canada_keywords": canada_keywords_found,
                "answer_immigration_keywords": immigration_keywords_found,
                "suggestion_issues": suggestion_issues,
                "score": response["score"]
            })
        else:
            results["passed"].append(question)
            results["details"].append({
                "question": question,
                "status": "PASSED",
                "score": response["score"]
            })
    
    return results

def test_canadian_recruiter_questions(
    openai_service: OpenAIService,
    direct_answer_storage: LocalEmbeddingStorage,
    direct_answer_service: DirectAnswerService
) -> Dict:
    """Test that Canadian recruiter questions DO mention Canada/immigration."""
    results = {
        "passed": [],
        "failed": [],
        "details": []
    }
    
    print("\n" + "="*80)
    print("TESTING CANADIAN RECRUITER QUESTIONS")
    print("="*80)
    print("These questions SHOULD mention Canada or immigration.\n")
    
    for question in CANADIAN_RECRUITER_QUESTIONS:
        response = get_direct_answer_response(
            question, openai_service, direct_answer_storage, direct_answer_service
        )
        
        if not response:
            results["failed"].append(question)
            results["details"].append({
                "question": question,
                "status": "FAILED",
                "reason": "No direct answer found"
            })
            continue
        
        answer = response["answer"]
        suggestions = response["suggestions"]
        
        canada_keywords_found = check_for_keywords(answer, CANADA_KEYWORDS)
        immigration_keywords_found = check_for_keywords(answer, IMMIGRATION_KEYWORDS)
        
        has_canada_or_immigration = bool(canada_keywords_found or immigration_keywords_found)
        
        if has_canada_or_immigration:
            results["passed"].append(question)
            results["details"].append({
                "question": question,
                "status": "PASSED",
                "canada_keywords": canada_keywords_found,
                "immigration_keywords": immigration_keywords_found,
                "score": response["score"]
            })
        else:
            results["failed"].append(question)
            results["details"].append({
                "question": question,
                "status": "FAILED",
                "reason": "No Canada or immigration keywords found",
                "score": response["score"]
            })
    
    return results

def generate_report(uk_results: Dict, canadian_results: Dict) -> str:
    """Generate a test report."""
    report = []
    report.append("\n" + "="*80)
    report.append("UK vs CANADIAN RECRUITER TEST REPORT")
    report.append("="*80)
    
    uk_total = len(UK_RECRUITER_QUESTIONS)
    uk_passed = len(uk_results["passed"])
    uk_failed = len(uk_results["failed"])
    uk_pass_rate = (uk_passed / uk_total * 100) if uk_total > 0 else 0
    
    canadian_total = len(CANADIAN_RECRUITER_QUESTIONS)
    canadian_passed = len(canadian_results["passed"])
    canadian_failed = len(canadian_results["failed"])
    canadian_pass_rate = (canadian_passed / canadian_total * 100) if canadian_total > 0 else 0
    
    report.append("\nUK RECRUITER QUESTIONS (Should NOT mention Canada/immigration):")
    report.append(f"  Total: {uk_total}")
    report.append(f"  Passed: {uk_passed} ({uk_pass_rate:.1f}%)")
    report.append(f"  Failed: {uk_failed}")
    
    report.append("\nCANADIAN RECRUITER QUESTIONS (Should mention Canada/immigration):")
    report.append(f"  Total: {canadian_total}")
    report.append(f"  Passed: {canadian_passed} ({canadian_pass_rate:.1f}%)")
    report.append(f"  Failed: {canadian_failed}")
    
    overall_total = uk_total + canadian_total
    overall_passed = uk_passed + canadian_passed
    overall_pass_rate = (overall_passed / overall_total * 100) if overall_total > 0 else 0
    
    report.append(f"\nOVERALL: {overall_passed}/{overall_total} passed ({overall_pass_rate:.1f}%)")
    
    if uk_results["failed"]:
        report.append("\n" + "-"*80)
        report.append("UK RECRUITER FAILURES (Should NOT mention Canada/immigration):")
        report.append("-"*80)
        for detail in uk_results["details"]:
            if detail["status"] == "FAILED":
                report.append(f"\n❌ {detail['question']}")
                if "reason" in detail:
                    report.append(f"   Reason: {detail['reason']}")
                if "answer_canada_keywords" in detail and detail["answer_canada_keywords"]:
                    report.append(f"   Canada keywords in answer: {detail['answer_canada_keywords']}")
                if "answer_immigration_keywords" in detail and detail["answer_immigration_keywords"]:
                    report.append(f"   Immigration keywords in answer: {detail['answer_immigration_keywords']}")
                if "suggestion_issues" in detail and detail["suggestion_issues"]:
                    report.append(f"   Issues in suggestions:")
                    for issue in detail["suggestion_issues"]:
                        report.append(f"     - '{issue['suggestion']}'")
                        if issue.get("canada_keywords"):
                            report.append(f"       Contains: {issue['canada_keywords']}")
                        if issue.get("immigration_keywords"):
                            report.append(f"       Contains: {issue['immigration_keywords']}")
                if "score" in detail:
                    report.append(f"   Score: {detail['score']:.3f}")
    
    if canadian_results["failed"]:
        report.append("\n" + "-"*80)
        report.append("CANADIAN RECRUITER FAILURES (Should mention Canada/immigration):")
        report.append("-"*80)
        for detail in canadian_results["details"]:
            if detail["status"] == "FAILED":
                report.append(f"\n❌ {detail['question']}")
                if "reason" in detail:
                    report.append(f"   Reason: {detail['reason']}")
                if "score" in detail:
                    report.append(f"   Score: {detail['score']:.3f}")
    
    if uk_results["passed"]:
        report.append("\n" + "-"*80)
        report.append("UK RECRUITER PASSES:")
        report.append("-"*80)
        for detail in uk_results["details"]:
            if detail["status"] == "PASSED":
                report.append(f"✓ {detail['question']} (score: {detail.get('score', 0):.3f})")
    
    if canadian_results["passed"]:
        report.append("\n" + "-"*80)
        report.append("CANADIAN RECRUITER PASSES:")
        report.append("-"*80)
        for detail in canadian_results["details"]:
            if detail["status"] == "PASSED":
                keywords = []
                if detail.get("canada_keywords"):
                    keywords.extend(detail["canada_keywords"])
                if detail.get("immigration_keywords"):
                    keywords.extend(detail["immigration_keywords"])
                keyword_str = ", ".join(keywords) if keywords else "None"
                report.append(f"✓ {detail['question']} (score: {detail.get('score', 0):.3f}, keywords: {keyword_str})")
    
    return "\n".join(report)

def main():
    print("Initializing services...")
    openai_service = OpenAIService()
    
    direct_answer_embeddings_file = Path(__file__).parent.parent / "direct-answer-embeddings.json"
    direct_answer_storage = LocalEmbeddingStorage(storage_path=str(direct_answer_embeddings_file))
    direct_answer_service = DirectAnswerService()
    
    if not direct_answer_embeddings_file.exists():
        print(f"ERROR: Direct answer embeddings file not found: {direct_answer_embeddings_file}")
        print("Please run embed_direct_answers.py first.")
        return
    
    print(f"Loaded {len(direct_answer_storage.embeddings)} direct answer embeddings")
    
    print("\nRunning UK recruiter tests...")
    uk_results = test_uk_recruiter_questions(
        openai_service, direct_answer_storage, direct_answer_service
    )
    
    print("\nRunning Canadian recruiter tests...")
    canadian_results = test_canadian_recruiter_questions(
        openai_service, direct_answer_storage, direct_answer_service
    )
    
    report = generate_report(uk_results, canadian_results)
    print(report)
    
    report_file = Path(__file__).parent.parent / "test_uk_vs_canada_report.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n\nReport saved to: {report_file}")
    
    if uk_results["failed"] or canadian_results["failed"]:
        print("\n⚠️  Some tests failed. Review the report above.")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()

