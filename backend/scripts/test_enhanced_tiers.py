import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent))

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage
from app.services.profanity_filter import ProfanityFilter

load_dotenv()

EMBEDDINGS_FILE = Path(__file__).parent.parent / "embeddings.json"

VERY_LOW_THRESHOLD = 0.20
CONFIDENCE_THRESHOLD = 0.40

TEST_CASES = {
    "PROFANITY/ABUSE (Expected: Boundary Setting)": [
        "This chatbot is fucking useless",
        "Your projects are shit",
        "Tell me about your stupid work",
        "What the fuck is this garbage?",
        "You're a terrible developer",
    ],
    
    "OFF-TOPIC (Expected: Off-Topic Response, Score <0.20)": [
        "Tell me about penguins",
        "What's the weather like in Tokyo?",
        "Who won the World Cup in 2022?",
        "What's the capital of France?",
        "How do I bake a chocolate cake?",
    ],
    
    "WEAK COVERAGE (Expected: Redirect, Score 0.20-0.39)": [
        "What's your typical workday like?",
        "What conferences do you attend?",
        "What's your management style?",
        "What are your salary expectations?",
        "How would your colleagues describe you?",
    ],
    
    "STRONG COVERAGE (Expected: Full Answer, Score ≥0.40)": [
        "Tell me about WhatNow",
        "What's your Python experience?",
        "How do you approach problem-solving?",
        "Tell me about your React experience",
        "Why did you build your portfolio projects?",
    ],
}

def determine_mode(question, similar_notes, top_score, profanity_filter):
    profanity_check = profanity_filter.check_question(question)
    
    if profanity_check["has_profanity"]:
        return "boundary_setting"
    elif top_score < VERY_LOW_THRESHOLD:
        return "off_topic"
    elif top_score < CONFIDENCE_THRESHOLD:
        return "redirect"
    else:
        return "full_answer"

def test_question(question: str, openai_service, embedding_storage, profanity_filter):
    query_embedding = openai_service.get_embedding(question)
    similar_notes = embedding_storage.query_similar(query_embedding, top_k=5)
    
    if not similar_notes:
        return None, 0.0, [], "error"
    
    top_score = similar_notes[0]['score']
    mode = determine_mode(question, similar_notes, top_score, profanity_filter)
    
    top_note_ids = [note['id'] for note in similar_notes[:3]]
    
    if mode == "boundary_setting":
        response = openai_service.generate_boundary_response()
    elif mode == "off_topic":
        response = openai_service.generate_off_topic_response()
    elif mode == "redirect":
        context = "\n\n".join([
            note['metadata'].get('content_preview', '')[:200] 
            for note in similar_notes
        ])
        response = openai_service.generate_redirect_response(question, context)
    else:
        context = "\n\n".join([
            note['metadata'].get('content_preview', '')[:200] 
            for note in similar_notes
        ])
        response = openai_service.generate_chat_response(question, context)
    
    return response, top_score, top_note_ids, mode

def print_separator(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def main():
    print("Initializing services...")
    openai_service = OpenAIService()
    embedding_storage = LocalEmbeddingStorage(storage_path=str(EMBEDDINGS_FILE))
    profanity_filter = ProfanityFilter()
    
    note_count = embedding_storage.get_stats()['total_notes']
    print(f"Loaded {note_count} notes")
    print(f"Very Low Threshold: {VERY_LOW_THRESHOLD}")
    print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}\n")
    
    results_summary = {
        "boundary_setting": {"expected": 0, "correct": 0, "incorrect": 0},
        "off_topic": {"expected": 0, "correct": 0, "incorrect": 0},
        "redirect": {"expected": 0, "correct": 0, "incorrect": 0},
        "full_answer": {"expected": 0, "correct": 0, "incorrect": 0},
    }
    
    mode_map = {
        "PROFANITY/ABUSE (Expected: Boundary Setting)": "boundary_setting",
        "OFF-TOPIC (Expected: Off-Topic Response, Score <0.20)": "off_topic",
        "WEAK COVERAGE (Expected: Redirect, Score 0.20-0.39)": "redirect",
        "STRONG COVERAGE (Expected: Full Answer, Score ≥0.40)": "full_answer",
    }
    
    for category, questions in TEST_CASES.items():
        print_separator(category)
        expected_mode = mode_map[category]
        results_summary[expected_mode]["expected"] += len(questions)
        
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}] Q: {question}")
            print("-" * 80)
            
            response, top_score, top_notes, actual_mode = test_question(
                question, openai_service, embedding_storage, profanity_filter
            )
            
            if response is None:
                print("ERROR: No notes retrieved")
                continue
            
            print(f"Top Score: {top_score:.4f}")
            print(f"Mode: {actual_mode}")
            print(f"Top 3 Notes: {', '.join(top_notes)}")
            
            if actual_mode == expected_mode:
                results_summary[expected_mode]["correct"] += 1
                status = "✅ CORRECT"
            else:
                results_summary[expected_mode]["incorrect"] += 1
                status = f"❌ INCORRECT (Expected: {expected_mode}, Got: {actual_mode})"
            
            print(f"Status: {status}")
            
            print(f"\nResponse Preview:")
            print(response[:300] + "..." if len(response) > 300 else response)
    
    print_separator("SUMMARY")
    
    total_expected = sum(cat["expected"] for cat in results_summary.values())
    total_correct = sum(cat["correct"] for cat in results_summary.values())
    accuracy = (total_correct / total_expected * 100) if total_expected > 0 else 0
    
    print(f"Overall Accuracy: {total_correct}/{total_expected} ({accuracy:.1f}%)\n")
    
    for mode, stats in results_summary.items():
        if stats["expected"] > 0:
            mode_accuracy = (stats["correct"] / stats["expected"] * 100)
            print(f"{mode.upper()}")
            print(f"  Expected: {stats['expected']}")
            print(f"  Correct: {stats['correct']}")
            print(f"  Incorrect: {stats['incorrect']}")
            print(f"  Accuracy: {mode_accuracy:.1f}%")
            print()
    
    print("\n" + "="*80)
    print("ASSESSMENT")
    print("="*80 + "\n")
    
    if accuracy >= 90:
        print("✅ EXCELLENT: Tier system working as expected")
    elif accuracy >= 75:
        print("⚠️  GOOD: Minor tuning needed")
    elif accuracy >= 60:
        print("⚠️  FAIR: Threshold adjustment recommended")
    else:
        print("❌ POOR: Significant issues - review thresholds")
    
    print(f"\nKey Metrics:")
    print(f"  - Profanity Detection: {results_summary['boundary_setting']['correct']}/{results_summary['boundary_setting']['expected']}")
    print(f"  - Off-Topic Detection: {results_summary['off_topic']['correct']}/{results_summary['off_topic']['expected']}")
    print(f"  - Redirect Routing: {results_summary['redirect']['correct']}/{results_summary['redirect']['expected']}")
    print(f"  - Full Answer Routing: {results_summary['full_answer']['correct']}/{results_summary['full_answer']['expected']}")
    
    print("\n" + "="*80)
    print("Test Complete!")
    print("="*80)

if __name__ == "__main__":
    main()

