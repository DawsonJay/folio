import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Tuple

sys.path.append(str(Path(__file__).parent.parent))

load_dotenv(Path(__file__).parent.parent / ".env")

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage

TARGET_QUESTION = "Tell me about yourself"
DIRECT_ANSWER_THRESHOLD = 0.75
BORDERLINE_LOW = 0.50

TEST_QUESTIONS = {
    "Category 1: Close Matches (Expected: >= 0.75)": [
        "Tell me about yourself",
        "Can you tell me about yourself?",
        "Tell me about yourself, please",
        "I'd like to know more about you",
        "Can you introduce yourself?",
        "Tell me a bit about yourself",
        "What can you tell me about yourself?",
    ],
    "Category 2: Moderate Variations (Expected: 0.50-0.75)": [
        "Who are you?",
        "What's your background?",
        "Give me an overview of yourself",
        "Describe yourself",
        "What should I know about you?",
        "Tell me about your background",
    ],
    "Category 3: Different Questions (Expected: < 0.50)": [
        "What languages do you know?",
        "What projects have you built?",
        "Why are you looking for a new role?",
        "What's your favorite color?",
        "How do you approach problem-solving?",
        "What technologies do you use?",
    ]
}

def find_target_embedding(storage: LocalEmbeddingStorage, target_question: str) -> Tuple[str, List[float]]:
    """Find the embedding for the target question in direct answer storage."""
    for note_id, data in storage.embeddings.items():
        metadata = data.get("metadata", {})
        if metadata.get("question") == target_question:
            return note_id, data["embedding"]
    
    raise ValueError(f"Target question '{target_question}' not found in direct answer embeddings")

def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Calculate cosine similarity between two embeddings."""
    import numpy as np
    v1 = np.array(embedding1)
    v2 = np.array(embedding2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def categorize_score(score: float) -> Tuple[str, str]:
    """Categorize a similarity score."""
    if score >= DIRECT_ANSWER_THRESHOLD:
        return "✓", "MATCH"
    elif score >= BORDERLINE_LOW:
        return "?", "BORDERLINE"
    else:
        return "✗", "NO MATCH"

def main():
    print(f"Testing Direct Answer Matching: \"{TARGET_QUESTION}\"")
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
    
    try:
        target_note_id, target_embedding = find_target_embedding(storage, TARGET_QUESTION)
        print(f"Found target question: \"{TARGET_QUESTION}\" (ID: {target_note_id})")
        print()
    except ValueError as e:
        print(f"ERROR: {e}")
        return
    
    results = {}
    all_scores = []
    
    for category, questions in TEST_QUESTIONS.items():
        print(category)
        print("-" * 80)
        
        category_scores = []
        category_results = []
        
        for question in questions:
            test_embedding = openai_service.get_embedding(question)
            score = calculate_similarity(target_embedding, test_embedding)
            category_scores.append(score)
            all_scores.append(score)
            
            symbol, status = categorize_score(score)
            category_results.append((question, score, symbol, status))
            
            print(f"{symbol} \"{question}\"")
            print(f"  → {score:.3f} ({status})")
        
        results[category] = {
            "scores": category_scores,
            "results": category_results
        }
        
        avg_score = sum(category_scores) / len(category_scores) if category_scores else 0
        print(f"  Average score: {avg_score:.3f}")
        print()
    
    print("=" * 80)
    print("Summary:")
    print("-" * 80)
    
    category1_results = results["Category 1: Close Matches (Expected: >= 0.75)"]
    category1_matches = sum(1 for _, score, _, _ in category1_results['results'] if score >= DIRECT_ANSWER_THRESHOLD)
    print(f"- Close matches: {category1_matches}/{len(category1_results['results'])} matched (>= {DIRECT_ANSWER_THRESHOLD})")
    
    category2_results = results["Category 2: Moderate Variations (Expected: 0.50-0.75)"]
    category2_in_range = sum(1 for _, score, _, _ in category2_results['results'] if BORDERLINE_LOW <= score < DIRECT_ANSWER_THRESHOLD)
    print(f"- Borderline: {category2_in_range}/{len(category2_results['results'])} in range ({BORDERLINE_LOW}-{DIRECT_ANSWER_THRESHOLD})")
    
    category3_results = results["Category 3: Different Questions (Expected: < 0.50)"]
    category3_rejected = sum(1 for _, score, _, _ in category3_results['results'] if score < BORDERLINE_LOW)
    print(f"- Different questions: {category3_rejected}/{len(category3_results['results'])} correctly rejected (< {BORDERLINE_LOW})")
    
    print()
    
    if category1_matches == len(category1_results['results']) and category3_rejected == len(category3_results['results']):
        print(f"✓ Threshold {DIRECT_ANSWER_THRESHOLD} appears appropriate")
    else:
        print(f"? Consider adjusting threshold {DIRECT_ANSWER_THRESHOLD}")
        if category1_matches < len(category1_results['results']):
            min_close_score = min(score for _, score, _, _ in category1_results['results'])
            print(f"  - Some close matches scored below threshold (min: {min_close_score:.3f})")
        if category3_rejected < len(category3_results['results']):
            max_different_score = max(score for _, score, _, _ in category3_results['results'])
            print(f"  - Some different questions scored above {BORDERLINE_LOW} (max: {max_different_score:.3f})")

if __name__ == "__main__":
    main()

