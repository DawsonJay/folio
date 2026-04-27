import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Tuple, Optional, Any
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

load_dotenv(Path(__file__).parent.parent / ".env")

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage

DIRECT_ANSWER_THRESHOLD = 0.75
BORDERLINE_LOW = 0.50

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.confusion_cases = []
        self.score_distributions = []
        self.details = []

def load_all_direct_answers(storage: LocalEmbeddingStorage) -> Dict[str, Dict[str, Any]]:
    """Load all direct answer embeddings with their metadata."""
    all_answers = {}
    for note_id, data in storage.embeddings.items():
        metadata = data.get("metadata", {})
        question = metadata.get("question", "")
        if question:
            all_answers[question] = {
                "id": note_id,
                "embedding": data["embedding"],
                "file_path": metadata.get("file_path", ""),
                "metadata": metadata
            }
    return all_answers

def find_direct_answer_by_title(storage: LocalEmbeddingStorage, question_title: str) -> Optional[Dict[str, Any]]:
    """Find a direct answer embedding by its question title."""
    for note_id, data in storage.embeddings.items():
        metadata = data.get("metadata", {})
        if metadata.get("question") == question_title:
            return {
                "id": note_id,
                "embedding": data["embedding"],
                "file_path": metadata.get("file_path", ""),
                "metadata": metadata
            }
    return None

def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Calculate cosine similarity between two embeddings."""
    v1 = np.array(embedding1)
    v2 = np.array(embedding2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def query_similar_questions(
    storage: LocalEmbeddingStorage,
    query_embedding: List[float],
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """Query for similar questions and return top_k results."""
    results = []
    for note_id, data in storage.embeddings.items():
        embedding = data["embedding"]
        metadata = data.get("metadata", {})
        similarity = calculate_similarity(query_embedding, embedding)
        results.append({
            "id": note_id,
            "question": metadata.get("question", ""),
            "score": similarity,
            "file_path": metadata.get("file_path", "")
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

def select_representative_sample(all_answers: Dict[str, Dict[str, Any]]) -> List[str]:
    """Select a representative sample of ~30 direct answers covering different question types."""
    sample = []
    
    categories = {
        "what": [],
        "how": [],
        "why": [],
        "tell_me": [],
        "do_you": [],
        "have_you": [],
        "are_you": [],
        "when": [],
        "where": []
    }
    
    for question in all_answers.keys():
        question_lower = question.lower()
        if question_lower.startswith("what"):
            categories["what"].append(question)
        elif question_lower.startswith("how"):
            categories["how"].append(question)
        elif question_lower.startswith("why"):
            categories["why"].append(question)
        elif question_lower.startswith("tell me"):
            categories["tell_me"].append(question)
        elif question_lower.startswith("do you"):
            categories["do_you"].append(question)
        elif question_lower.startswith("have you"):
            categories["have_you"].append(question)
        elif question_lower.startswith("are you"):
            categories["are_you"].append(question)
        elif question_lower.startswith("when"):
            categories["when"].append(question)
        elif question_lower.startswith("where"):
            categories["where"].append(question)
    
    target_per_category = 30 // len(categories)
    
    for category, questions in categories.items():
        if questions:
            sample.extend(questions[:target_per_category])
    
    if len(sample) < 30:
        remaining = [q for q in all_answers.keys() if q not in sample]
        sample.extend(remaining[:30 - len(sample)])
    
    return sample[:30]

def test_question_variations(
    openai_service: OpenAIService,
    storage: LocalEmbeddingStorage,
    target_question: str,
    variations: List[str],
    result: TestResult
) -> Dict[str, Any]:
    """Test variations of a question that should match the target."""
    target_data = find_direct_answer_by_title(storage, target_question)
    if not target_data:
        result.failed += len(variations)
        result.details.append(f"✗ Target question not found: {target_question}")
        return {"passed": 0, "failed": len(variations), "scores": []}
    
    target_embedding = target_data["embedding"]
    test_results = []
    passed = 0
    failed = 0
    scores = []
    
    for variation in variations:
        test_embedding = openai_service.get_embedding(variation)
        score = calculate_similarity(target_embedding, test_embedding)
        scores.append(score)
        
        if score >= DIRECT_ANSWER_THRESHOLD:
            passed += 1
            result.passed += 1
            test_results.append({"variation": variation, "score": score, "status": "PASS"})
        else:
            failed += 1
            result.failed += 1
            test_results.append({"variation": variation, "score": score, "status": "FAIL"})
            result.details.append(
                f"✗ Variation failed: '{variation}' scored {score:.3f} (expected >= {DIRECT_ANSWER_THRESHOLD})"
            )
    
    result.score_distributions.extend(scores)
    return {"passed": passed, "failed": failed, "scores": scores, "results": test_results}

def test_similar_question_pairs(
    openai_service: OpenAIService,
    storage: LocalEmbeddingStorage,
    question1: str,
    question2: str,
    expected_different: bool,
    result: TestResult
) -> Dict[str, Any]:
    """Test that similar questions either match different answers or one falls below threshold."""
    embedding1 = openai_service.get_embedding(question1)
    embedding2 = openai_service.get_embedding(question2)
    
    results1 = query_similar_questions(storage, embedding1, top_k=3)
    results2 = query_similar_questions(storage, embedding2, top_k=3)
    
    top1 = results1[0] if results1 else None
    top2 = results2[0] if results2 else None
    
    if not top1 or not top2:
        result.failed += 1
        result.details.append(f"✗ Could not find matches for question pair: '{question1}' / '{question2}'")
        return {"status": "FAIL", "reason": "No matches found"}
    
    score1 = top1["score"]
    score2 = top2["score"]
    question1_match = top1["question"]
    question2_match = top2["question"]
    
    if expected_different:
        if question1_match != question2_match:
            result.passed += 1
            return {
                "status": "PASS",
                "question1_match": question1_match,
                "question2_match": question2_match,
                "score1": score1,
                "score2": score2
            }
        elif score1 < DIRECT_ANSWER_THRESHOLD or score2 < DIRECT_ANSWER_THRESHOLD:
            result.passed += 1
            return {
                "status": "PASS",
                "reason": "One question fell below threshold",
                "question1_match": question1_match,
                "question2_match": question2_match,
                "score1": score1,
                "score2": score2
            }
        else:
            result.failed += 1
            result.confusion_cases.append({
                "question1": question1,
                "question2": question2,
                "matched_same": True,
                "match": question1_match,
                "score1": score1,
                "score2": score2
            })
            result.details.append(
                f"✗ Confusion: '{question1}' and '{question2}' both matched '{question1_match}' "
                f"(scores: {score1:.3f}, {score2:.3f})"
            )
            return {
                "status": "FAIL",
                "reason": "Both matched same answer above threshold",
                "question1_match": question1_match,
                "question2_match": question2_match,
                "score1": score1,
                "score2": score2
            }
    else:
        if question1_match == question2_match and score1 >= DIRECT_ANSWER_THRESHOLD and score2 >= DIRECT_ANSWER_THRESHOLD:
            result.passed += 1
            return {
                "status": "PASS",
                "question1_match": question1_match,
                "question2_match": question2_match,
                "score1": score1,
                "score2": score2
            }
        else:
            result.failed += 1
            result.details.append(
                f"✗ Expected same match but got different: '{question1}' -> '{question1_match}' "
                f"({score1:.3f}), '{question2}' -> '{question2_match}' ({score2:.3f})"
            )
            return {
                "status": "FAIL",
                "question1_match": question1_match,
                "question2_match": question2_match,
                "score1": score1,
                "score2": score2
            }

def test_edge_cases(
    openai_service: OpenAIService,
    storage: LocalEmbeddingStorage,
    question: str,
    expected_matches: List[str],
    result: TestResult
) -> Dict[str, Any]:
    """Test ambiguous questions to see if correct answer appears in top results."""
    query_embedding = openai_service.get_embedding(question)
    results = query_similar_questions(storage, query_embedding, top_k=5)
    
    if not results:
        result.failed += 1
        result.details.append(f"✗ No matches found for edge case: '{question}'")
        return {"status": "FAIL", "reason": "No matches"}
    
    top_score = results[0]["score"]
    top_question = results[0]["question"]
    
    found_expected = False
    for expected in expected_matches:
        for r in results:
            if r["question"] == expected:
                found_expected = True
                if r == results[0]:
                    result.passed += 1
                    return {
                        "status": "PASS",
                        "top_match": top_question,
                        "top_score": top_score,
                        "expected_found": True,
                        "expected_in_top": True
                    }
                else:
                    result.passed += 1
                    return {
                        "status": "PASS",
                        "top_match": top_question,
                        "top_score": top_score,
                        "expected_found": True,
                        "expected_in_top": False,
                        "expected_position": next(i for i, r in enumerate(results) if r["question"] == expected) + 1
                    }
    
    if not found_expected:
        result.failed += 1
        result.confusion_cases.append({
            "question": question,
            "expected_matches": expected_matches,
            "actual_top": top_question,
            "top_score": top_score
        })
        result.details.append(
            f"✗ Edge case failed: '{question}' matched '{top_question}' ({top_score:.3f}), "
            f"expected one of {expected_matches}"
        )
        return {
            "status": "FAIL",
            "top_match": top_question,
            "top_score": top_score,
            "expected_matches": expected_matches
        }

def generate_report(result: TestResult) -> str:
    """Generate a comprehensive test report."""
    report = []
    report.append("=" * 80)
    report.append("TIER 1 DIRECT ANSWER MATCHING - COMPREHENSIVE TEST REPORT")
    report.append("=" * 80)
    report.append("")
    
    total = result.passed + result.failed
    pass_rate = (result.passed / total * 100) if total > 0 else 0
    
    report.append("SUMMARY")
    report.append("-" * 80)
    report.append(f"Total Tests: {total}")
    report.append(f"Passed: {result.passed} ({pass_rate:.1f}%)")
    report.append(f"Failed: {result.failed} ({100 - pass_rate:.1f}%)")
    report.append("")
    
    if result.score_distributions:
        scores = result.score_distributions
        report.append("SCORE DISTRIBUTION")
        report.append("-" * 80)
        report.append(f"Min: {min(scores):.3f}")
        report.append(f"Max: {max(scores):.3f}")
        report.append(f"Mean: {np.mean(scores):.3f}")
        report.append(f"Median: {np.median(scores):.3f}")
        report.append(f"Scores >= {DIRECT_ANSWER_THRESHOLD}: {sum(1 for s in scores if s >= DIRECT_ANSWER_THRESHOLD)}/{len(scores)}")
        report.append("")
    
    if result.confusion_cases:
        report.append("CONFUSION CASES")
        report.append("-" * 80)
        for i, case in enumerate(result.confusion_cases, 1):
            report.append(f"{i}. {case}")
        report.append("")
    
    if result.details:
        report.append("DETAILED RESULTS")
        report.append("-" * 80)
        for detail in result.details:
            report.append(detail)
        report.append("")
    
    report.append("RECOMMENDATIONS")
    report.append("-" * 80)
    if pass_rate >= 95:
        report.append("✓ Threshold appears appropriate - excellent pass rate")
    elif pass_rate >= 85:
        report.append("? Threshold may need minor adjustment - good pass rate")
    else:
        report.append("✗ Threshold may need significant adjustment - low pass rate")
    
    if result.confusion_cases:
        report.append("⚠ Found confusion cases - review similar question pairs")
    
    if result.score_distributions:
        scores = result.score_distributions
        below_threshold = [s for s in scores if s < DIRECT_ANSWER_THRESHOLD]
        if below_threshold:
            max_below = max(below_threshold)
            report.append(f"ℹ Highest score below threshold: {max_below:.3f}")
            if max_below >= BORDERLINE_LOW:
                report.append(f"  Consider if threshold should be lowered to {max_below:.2f}")
    
    report.append("")
    report.append("=" * 80)
    
    return "\n".join(report)

def main():
    print("Initializing Tier 1 Direct Answer Matching Comprehensive Test")
    print("=" * 80)
    print()
    
    direct_answer_embeddings_file = Path(__file__).parent.parent / "direct-answer-embeddings.json"
    
    if not direct_answer_embeddings_file.exists():
        print(f"ERROR: Direct answer embeddings file not found: {direct_answer_embeddings_file}")
        print("Please run: python scripts/embed_direct_answers.py")
        return
    
    print("Initializing services...")
    openai_service = OpenAIService()
    storage = LocalEmbeddingStorage(storage_path=str(direct_answer_embeddings_file))
    
    print(f"Loading direct answer embeddings from {direct_answer_embeddings_file}...")
    stats = storage.get_stats()
    print(f"Found {stats['total_notes']} direct answer embeddings")
    print()
    
    all_answers = load_all_direct_answers(storage)
    print(f"Loaded {len(all_answers)} direct answers")
    
    sample = select_representative_sample(all_answers)
    print(f"Selected {len(sample)} representative questions for testing")
    print()
    
    result = TestResult()
    
    print("=" * 80)
    print("TESTING: Correct Matching (Question Variations)")
    print("=" * 80)
    print()
    
    test_cases_correct = {
        "Tell me about yourself": [
            "Can you tell me about yourself?",
            "Tell me a bit about yourself",
            "I'd like to know more about you",
            "Can you introduce yourself?",
            "What can you tell me about yourself?"
        ],
        "What are your strongest technical skills?": [
            "What are your strongest skills?",
            "What technical skills are you strongest in?",
            "What are you best at technically?",
            "What are your main technical skills?"
        ],
        "Why are you looking for a new role?": [
            "Why are you looking for a new job?",
            "Why do you want to leave your current role?",
            "What's making you look for new opportunities?",
            "Why are you seeking a new position?"
        ],
        "Tell me about WhatNow": [
            "What is WhatNow?",
            "Can you tell me about WhatNow?",
            "Tell me about the WhatNow project",
            "What's WhatNow about?"
        ],
        "What languages do you know?": [
            "What programming languages do you know?",
            "What languages are you familiar with?",
            "What coding languages do you know?",
            "Which programming languages do you use?"
        ],
        "How do you approach problem-solving?": [
            "How do you solve problems?",
            "What's your approach to solving problems?",
            "How do you tackle problems?",
            "Tell me about your problem-solving approach"
        ],
        "What's your biggest weakness?": [
            "What are your weaknesses?",
            "What's your greatest weakness?",
            "What would you say is your biggest weakness?",
            "Tell me about your weaknesses"
        ],
        "Tell me about your experience with React": [
            "What's your React experience?",
            "How experienced are you with React?",
            "Tell me about your React skills",
            "What can you tell me about your React experience?"
        ],
        "What projects have you built?": [
            "What projects have you worked on?",
            "Tell me about your projects",
            "What have you built?",
            "What are some projects you've done?"
        ],
        "How do you work in a team?": [
            "How do you collaborate with others?",
            "Tell me about your teamwork",
            "How do you work with a team?",
            "What's your approach to teamwork?"
        ]
    }
    
    for target, variations in test_cases_correct.items():
        if target in all_answers:
            print(f"Testing: {target}")
            test_result = test_question_variations(openai_service, storage, target, variations, result)
            print(f"  Passed: {test_result['passed']}/{len(variations)}")
            if test_result['failed'] > 0:
                print(f"  Failed: {test_result['failed']}/{len(variations)}")
            print()
    
    print("=" * 80)
    print("TESTING: Similar But Different Questions")
    print("=" * 80)
    print()
    
    similar_pairs = [
        ("What's your background?", "What's your professional background?", True),
        ("Tell me about your experience", "Tell me about your current experience", True),
        ("What's your role?", "What's your current role?", True),
        ("Why are you looking for a new role?", "Why did you leave your last job?", True),
        ("What languages do you know?", "What programming languages are you most proficient in?", False),
        ("Tell me about your experience at Nurtur", "Tell me about your most recent role", True),
        ("What's your biggest weakness?", "What are your weaknesses?", False),
        ("How do you handle stress?", "How do you handle stress and pressure?", False),
        ("Tell me about your current role", "Tell me about your current experience", True),
        ("What's your story?", "What's your background?", True),
        ("How did you get into development?", "How did you transition from art to tech?", True),
        ("What are you passionate about?", "What motivates you as a developer?", True),
        ("Tell me about moh-ami", "Tell me about WhatNow", True),
        ("What's your frontend development experience?", "What's your backend development experience?", True),
        ("What's your experience with TypeScript?", "How comfortable are you with TypeScript?", False),
    ]
    
    for q1, q2, expected_different in similar_pairs:
        print(f"Testing pair: '{q1}' vs '{q2}'")
        test_result = test_similar_question_pairs(openai_service, storage, q1, q2, expected_different, result)
        print(f"  Status: {test_result['status']}")
        if test_result['status'] == "PASS":
            print(f"  ✓ Question 1 matched: {test_result.get('question1_match', 'N/A')} ({test_result.get('score1', 0):.3f})")
            print(f"  ✓ Question 2 matched: {test_result.get('question2_match', 'N/A')} ({test_result.get('score2', 0):.3f})")
        print()
    
    print("=" * 80)
    print("TESTING: Edge Cases (Ambiguous Questions)")
    print("=" * 80)
    print()
    
    edge_cases = [
        ("What's your experience?", ["Tell me about your current experience", "Tell me about your experience at Nurtur"]),
        ("Tell me about your background", ["What's your background?", "What's your professional background?"]),
        ("What projects have you worked on?", ["What projects have you built?", "Tell me about your projects"]),
        ("What's your role?", ["Tell me about your current role", "Tell me about your most recent role"]),
        ("How do you handle failure?", ["Tell me about a project that failed", "How do you handle failure?"]),
        ("Tell me about a challenging project", ["Tell me about a challenging project", "Describe a difficult situation and how you handled it"]),
    ]
    
    for question, expected_matches in edge_cases:
        print(f"Testing edge case: '{question}'")
        test_result = test_edge_cases(openai_service, storage, question, expected_matches, result)
        print(f"  Status: {test_result['status']}")
        if test_result['status'] == "PASS":
            print(f"  ✓ Top match: {test_result.get('top_match', 'N/A')} ({test_result.get('top_score', 0):.3f})")
            if test_result.get('expected_in_top'):
                print(f"  ✓ Expected match found in top position")
            else:
                print(f"  ✓ Expected match found at position {test_result.get('expected_position', 'N/A')}")
        print()
    
    print("=" * 80)
    print("GENERATING REPORT")
    print("=" * 80)
    print()
    
    report = generate_report(result)
    print(report)
    
    report_file = Path(__file__).parent.parent / "test_tier1_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\nReport saved to: {report_file}")

if __name__ == "__main__":
    main()

