import os
import sys
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent))

load_dotenv(Path(__file__).parent.parent / ".env")

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage

TEST_QUERIES = {
    "whatnow_focused": [
        "Tell me about WhatNow",
        "How does the two-layer learning work in WhatNow?",
        "Why did you build WhatNow?",
        "What was the biggest technical challenge in WhatNow?",
        "Show me the WhatNow demo",
        "How did you solve the dataset problem?",
    ],
    "general": [
        "What's your React experience?",
        "Tell me about your leadership style",
        "Why do you want to work in Canada?",
        "What projects have you built?",
        "What's your Python experience?",
        "Tell me about your educational background",
    ],
    "edge_cases": [
        "Tell me about a project using contextual bandits",
        "What Python projects have you built?",
        "How have you used AI in your work?",
        "Tell me about moh-ami",
        "How do you approach problem-solving?",
    ]
}

def test_query(query: str, openai_service: OpenAIService, storage: LocalEmbeddingStorage, top_k: int = 5) -> Dict:
    print(f"\n{'='*80}")
    print(f"Query: {query}")
    print(f"{'='*80}")
    
    query_embedding = openai_service.get_embedding(query)
    
    results = storage.query_similar(query_embedding, top_k=top_k)
    
    print(f"\nRetrieved {len(results)} notes:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['id']} (score: {result['score']:.4f})")
        print(f"     Category: {result['metadata'].get('category', 'unknown')}")
        print(f"     Preview: {result['metadata'].get('content_preview', '')[:100]}...")
    
    note_contents = [result['metadata'].get('content_preview', '') for result in results]
    context = "\n\n".join(note_contents)
    
    answer = openai_service.generate_chat_response(query, context)
    
    print(f"\nGenerated Answer:")
    print(f"{answer}")
    
    return {
        "query": query,
        "retrieved_notes": [r['id'] for r in results],
        "scores": [r['score'] for r in results],
        "answer": answer
    }

def analyze_results(results_by_category: Dict[str, List[Dict]]):
    print(f"\n\n{'='*80}")
    print("ANALYSIS")
    print(f"{'='*80}")
    
    print("\n## WhatNow-Focused Queries")
    print("Expected: Should retrieve mostly WhatNow notes (6-8 out of 5)")
    whatnow_results = results_by_category["whatnow_focused"]
    for result in whatnow_results:
        whatnow_count = sum(1 for note in result['retrieved_notes'] if 'whatnow' in note.lower())
        print(f"  '{result['query'][:50]}...': {whatnow_count}/5 WhatNow notes")
    
    print("\n## General Queries")
    print("Expected: Should retrieve 0-2 WhatNow notes (only if highly relevant)")
    general_results = results_by_category["general"]
    for result in general_results:
        whatnow_count = sum(1 for note in result['retrieved_notes'] if 'whatnow' in note.lower())
        print(f"  '{result['query'][:50]}...': {whatnow_count}/5 WhatNow notes")
    
    print("\n## Edge Cases")
    print("Expected: Mixed behavior depending on query specificity")
    edge_results = results_by_category["edge_cases"]
    for result in edge_results:
        whatnow_count = sum(1 for note in result['retrieved_notes'] if 'whatnow' in note.lower())
        print(f"  '{result['query'][:50]}...': {whatnow_count}/5 WhatNow notes")
    
    print("\n## Overall Assessment")
    all_whatnow_queries = whatnow_results
    avg_whatnow_in_whatnow_queries = sum(
        sum(1 for note in r['retrieved_notes'] if 'whatnow' in note.lower())
        for r in all_whatnow_queries
    ) / len(all_whatnow_queries)
    
    all_general_queries = general_results
    avg_whatnow_in_general_queries = sum(
        sum(1 for note in r['retrieved_notes'] if 'whatnow' in note.lower())
        for r in all_general_queries
    ) / len(all_general_queries)
    
    print(f"Average WhatNow notes in WhatNow queries: {avg_whatnow_in_whatnow_queries:.2f}/5")
    print(f"Average WhatNow notes in general queries: {avg_whatnow_in_general_queries:.2f}/5")
    
    print("\n✅ Good signs:")
    if avg_whatnow_in_whatnow_queries >= 3.0:
        print(f"  ✓ WhatNow queries retrieve WhatNow notes ({avg_whatnow_in_whatnow_queries:.2f}/5)")
    else:
        print(f"  ✗ WhatNow queries not retrieving enough WhatNow notes ({avg_whatnow_in_whatnow_queries:.2f}/5)")
    
    if avg_whatnow_in_general_queries <= 2.0:
        print(f"  ✓ General queries avoid over-representing WhatNow ({avg_whatnow_in_general_queries:.2f}/5)")
    else:
        print(f"  ✗ General queries over-retrieve WhatNow notes ({avg_whatnow_in_general_queries:.2f}/5)")

def main():
    print("Initializing services...")
    openai_service = OpenAIService()
    storage = LocalEmbeddingStorage()
    
    stats = storage.get_stats()
    print(f"\nStorage stats: {stats}")
    
    if stats.get('total_notes', 0) == 0:
        print("\n❌ No embeddings found!")
        print("Run 'python scripts/embed_notes.py' first to embed the notes.")
        return
    
    print(f"\nRunning {sum(len(queries) for queries in TEST_QUERIES.values())} test queries...")
    
    results_by_category = {}
    
    for category, queries in TEST_QUERIES.items():
        print(f"\n\n{'#'*80}")
        print(f"# {category.upper().replace('_', ' ')} QUERIES")
        print(f"{'#'*80}")
        
        category_results = []
        for query in queries:
            result = test_query(query, openai_service, storage)
            category_results.append(result)
        
        results_by_category[category] = category_results
    
    analyze_results(results_by_category)
    
    print(f"\n\n{'='*80}")
    print("Test complete! Review the results above.")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()

