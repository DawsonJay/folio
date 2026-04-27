import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any

sys.path.append(str(Path(__file__).parent.parent))

load_dotenv(Path(__file__).parent.parent / ".env")

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage
from app.services.direct_answer_service import DirectAnswerService
from app.api.chat import chat, ChatRequest

DIRECT_ANSWER_MODES = ("direct_answer", "direct_answer_llm_match")

TEST_QUESTIONS = {
    "Should Match Direct Answer (Tier 1)": [
        "Tell me about yourself",
        "Can you tell me about yourself?",
        "Tell me a bit about yourself",
    ],
    "Should Fall Through to RAG (Tier 2)": [
        "What languages do you know?",
        "What projects have you built?",
        "Why are you looking for a new role?",
        "What technologies do you use?",
        "How did you transition from art to tech?",
        "Tell me about your work experience",
    ],
    "Edge Cases (Borderline)": [
        "I'd like to know more about you",  # Should fall through (0.590)
        "Who are you?",  # Should fall through (0.534)
        "What's your background?",  # Should fall through (0.478)
    ]
}

async def test_question(question: str) -> Dict[str, Any]:
    """Test a single question through the full chat endpoint."""
    request = ChatRequest(question=question)
    response = await chat(request)
    
    return {
        "question": question,
        "confidence": response.confidence,
        "top_score": response.top_score,
        "answer_preview": response.answer[:100] + "..." if len(response.answer) > 100 else response.answer,
        "emotion": response.emotion,
        "suggestions_count": len(response.suggestions),
        "has_project_links": response.projectLinks is not None
    }

async def main():
    print("Testing Tiered System: Direct Answers + RAG Fallback")
    print("=" * 80)
    print()
    
    # Check if embeddings exist
    embeddings_file = Path(__file__).parent.parent / "embeddings.json"
    direct_answer_embeddings_file = Path(__file__).parent.parent / "direct-answer-embeddings.json"
    
    if not embeddings_file.exists():
        print(f"ERROR: Main embeddings file not found: {embeddings_file}")
        print("Please run the embedding script for atomic notes first.")
        return
    
    if not direct_answer_embeddings_file.exists():
        print(f"ERROR: Direct answer embeddings file not found: {direct_answer_embeddings_file}")
        print("Please run: python scripts/embed_direct_answers.py")
        return
    
    print("Initializing services...")
    print()
    
    results = {}
    
    for category, questions in TEST_QUESTIONS.items():
        print(category)
        print("-" * 80)
        
        category_results = []
        
        for question in questions:
            print(f"Testing: \"{question}\"")
            result = await test_question(question)
            category_results.append(result)
            
            # Determine expected behavior
            if category == "Should Match Direct Answer (Tier 1)":
                status = "✓" if result["confidence"] in DIRECT_ANSWER_MODES else "✗"
            elif category == "Should Fall Through to RAG (Tier 2)":
                expected = ["high", "medium", "redirect", "off_topic"]
                status = "✓" if result["confidence"] in expected else "✗"
            else:  # Edge Cases (borderline; Tier 1.5 may map to a direct answer)
                expected = ["high", "medium", "redirect", "off_topic"] + list(DIRECT_ANSWER_MODES)
                status = "✓" if result["confidence"] in expected else "?"
            
            print(f"  {status} Confidence: {result['confidence']} (score: {result['top_score']:.3f})")
            print(f"    Answer: {result['answer_preview']}")
            print(f"    Emotion: {result['emotion']}, Suggestions: {result['suggestions_count']}")
            print()
        
        results[category] = category_results
    
    print("=" * 80)
    print("Summary:")
    print("-" * 80)
    
    # Tier 1 + 1.5 (Direct answer files)
    tier1_results = results["Should Match Direct Answer (Tier 1)"]
    tier1_matches = sum(1 for r in tier1_results if r["confidence"] in DIRECT_ANSWER_MODES)
    print(f"Direct answer (Tier 1/1.5): {tier1_matches}/{len(tier1_results)} correctly matched")
    
    # Tier 2 (RAG Fallback) — not a scripted direct answer
    tier2_results = results["Should Fall Through to RAG (Tier 2)"]
    tier2_fallthrough = sum(
        1 for r in tier2_results if r["confidence"] not in DIRECT_ANSWER_MODES
    )
    print(f"Tier 2 (RAG Fallback): {tier2_fallthrough}/{len(tier2_results)} correctly fell through")
    
    # Edge Cases
    edge_results = results["Edge Cases (Borderline)"]
    edge_fallthrough = sum(1 for r in edge_results if r["confidence"] in ["high", "medium", "redirect", "off_topic"])
    print(f"Edge Cases: {edge_fallthrough}/{len(edge_results)} correctly fell through")
    
    print()
    
    # Overall assessment
    total_tests = len(tier1_results) + len(tier2_results) + len(edge_results)
    total_correct = tier1_matches + tier2_fallthrough + edge_fallthrough
    
    print(f"Overall: {total_correct}/{total_tests} tests passed")
    
    if total_correct == total_tests:
        print("✓ All tests passed! Tiered system is working correctly.")
    else:
        print("? Some tests need review. Check individual results above.")

if __name__ == "__main__":
    asyncio.run(main())

