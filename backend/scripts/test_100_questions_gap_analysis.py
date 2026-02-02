import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
from collections import defaultdict

sys.path.append(str(Path(__file__).parent.parent))

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage
from dotenv import load_dotenv

load_dotenv()

EMBEDDINGS_FILE = Path(__file__).parent.parent / "embeddings.json"

VERY_LOW_THRESHOLD = 0.20
CONFIDENCE_THRESHOLD = 0.40

RECRUITER_QUESTIONS = {
    "Background & Introduction": [
        "Tell me about yourself",
        "What's your background?",
        "How did you get into development?",
        "What's your story?",
        "Walk me through your career journey",
        "How did you transition from art to tech?",
        "What brought you to software development?",
        "Tell me about your educational background",
        "What's your professional background?",
        "How would you describe yourself?",
    ],
    
    "Technical Skills - General": [
        "What programming languages are you most proficient in?",
        "Tell me about your experience with React",
        "What's your experience with Python?",
        "How comfortable are you with TypeScript?",
        "What databases have you worked with?",
        "Tell me about your frontend development experience",
        "What's your backend development experience?",
        "Have you worked with GraphQL?",
        "What's your experience with REST APIs?",
        "Tell me about your testing practices",
        "What CSS frameworks have you used?",
        "Do you have experience with Docker?",
        "What state management libraries do you know?",
        "Tell me about your JavaScript experience",
        "What build tools are you familiar with?",
    ],
    
    "AI/ML Specific": [
        "What AI/ML experience do you have?",
        "Tell me about a machine learning project you've built",
        "Do you have experience with LLMs?",
        "What's your understanding of embeddings?",
        "Have you worked with recommendation systems?",
        "Tell me about contextual bandits",
        "What's your experience with RAG systems?",
        "How do you approach AI project scoping?",
        "What AI frameworks have you used?",
        "Tell me about prompt engineering experience",
    ],
    
    "Projects": [
        "Tell me about your most successful project",
        "What's the most complex system you've built?",
        "Tell me about WhatNow",
        "Tell me about moh-ami",
        "Tell me about Atlantis",
        "What project are you most proud of?",
        "Tell me about a project that failed",
        "What's your current work project?",
        "Show me examples of your work",
        "Which project best demonstrates your skills?",
        "Tell me about Cirrus",
        "What projects have you built?",
        "Tell me about a challenging project",
        "What's your favorite project?",
        "Tell me about a project you learned from",
    ],
    
    "Work Experience": [
        "Tell me about your current role",
        "What do you do at Nurtur?",
        "Tell me about the Integrations Dashboard",
        "Tell me about the Nexus Dashboard",
        "Tell me about the Email Editor project",
        "What are your responsibilities at work?",
        "How long have you been a developer?",
        "What was your first development job?",
        "Tell me about your freelance experience",
        "Why did you leave your previous job?",
    ],
    
    "Problem Solving & Process": [
        "How do you approach problem-solving?",
        "Walk me through your development process",
        "How do you handle ambiguous requirements?",
        "Tell me about debugging a complex issue",
        "How do you prioritize tasks?",
        "What's your approach to learning new technologies?",
        "How do you make technical decisions?",
        "Tell me about balancing quality and speed",
        "How do you handle scope creep?",
        "What's your testing strategy?",
    ],
    
    "Teamwork & Collaboration": [
        "Tell me about your leadership style",
        "How do you work in a team?",
        "Have you mentored other developers?",
        "How do you handle disagreements with teammates?",
        "Tell me about collaborating with non-technical people",
        "What's your experience with code reviews?",
        "How do you communicate technical concepts?",
        "Tell me about a successful team project",
        "What makes you a good team member?",
        "How do you help struggling team members?",
    ],
    
    "Career Goals & Motivation": [
        "Why are you looking for a new role?",
        "What are your career goals?",
        "What are you looking for in your next role?",
        "Why should we hire you?",
        "What motivates you?",
        "What drives you as a developer?",
        "Where do you see yourself in 5 years?",
        "What are you looking for in a company?",
        "Why are you interested in this role?",
        "What makes you unique?",
    ],
    
    "Work Style & Preferences": [
        "Are you open to remote work?",
        "What's your ideal work environment?",
        "How do you handle work-life balance?",
        "What's your work style?",
        "How do you prefer to communicate?",
    ],
    
    "Salary & Logistics": [
        "What are your salary expectations?",
        "When can you start?",
        "Are you willing to relocate?",
        "What's your availability?",
        "Do you have any questions for us?",
    ],
}

def get_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")

def categorize_coverage(top_score: float, notes_retrieved: List[Dict]) -> str:
    if not notes_retrieved or top_score < VERY_LOW_THRESHOLD:
        return "no_coverage"
    elif top_score < CONFIDENCE_THRESHOLD:
        return "poor_coverage"
    else:
        return "good_coverage"

def analyze_question(
    question: str,
    category: str,
    openai_service: OpenAIService,
    embedding_storage: LocalEmbeddingStorage
) -> Dict[str, Any]:
    query_embedding = openai_service.get_embedding(question)
    similar_notes = embedding_storage.query_similar(query_embedding, top_k=5)
    
    top_score = similar_notes[0]['score'] if similar_notes else 0.0
    
    notes_data = [
        {
            "id": note['id'],
            "score": float(note['score']),
            "title": note['metadata'].get('title', note['id'])
        }
        for note in similar_notes
    ]
    
    coverage = categorize_coverage(top_score, similar_notes)
    
    return {
        "question": question,
        "category": category,
        "top_score": float(top_score),
        "coverage": coverage,
        "notes_retrieved": notes_data,
        "num_notes": len(similar_notes)
    }

def main():
    print("=" * 80)
    print("  100 Recruiter Questions Gap Analysis")
    print("=" * 80)
    print(f"\nEmbeddings file: {EMBEDDINGS_FILE}")
    print(f"Very Low Threshold: {VERY_LOW_THRESHOLD}")
    print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}\n")
    
    print("Initializing services...")
    openai_service = OpenAIService()
    embedding_storage = LocalEmbeddingStorage(storage_path=str(EMBEDDINGS_FILE))
    
    stats = embedding_storage.get_stats()
    print(f"Loaded {stats['total_notes']} notes\n")
    
    all_questions = []
    for category, questions in RECRUITER_QUESTIONS.items():
        for question in questions:
            all_questions.append((question, category))
    
    total_questions = len(all_questions)
    print(f"Total questions to analyze: {total_questions}\n")
    print("=" * 80)
    
    results = []
    category_stats = defaultdict(lambda: {"no_coverage": 0, "poor_coverage": 0, "good_coverage": 0})
    
    for i, (question, category) in enumerate(all_questions, 1):
        print(f"\n[{i}/{total_questions}] {category}: {question}")
        
        try:
            result = analyze_question(question, category, openai_service, embedding_storage)
            results.append(result)
            
            category_stats[category][result["coverage"]] += 1
            
            print(f"  Top Score: {result['top_score']:.4f} | Coverage: {result['coverage']}")
            if result['notes_retrieved']:
                top_note = result['notes_retrieved'][0]
                print(f"  Top Note: {top_note['id']} ({top_note['score']:.4f})")
            
            time.sleep(0.1)
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            results.append({
                "question": question,
                "category": category,
                "top_score": 0.0,
                "coverage": "error",
                "notes_retrieved": [],
                "num_notes": 0,
                "error": str(e)
            })
    
    no_coverage = [r for r in results if r["coverage"] == "no_coverage"]
    poor_coverage = [r for r in results if r["coverage"] == "poor_coverage"]
    good_coverage = [r for r in results if r["coverage"] == "good_coverage"]
    
    summary = {
        "no_coverage": len(no_coverage),
        "poor_coverage": len(poor_coverage),
        "good_coverage": len(good_coverage),
        "by_category": {
            cat: {
                "no_coverage": stats["no_coverage"],
                "poor_coverage": stats["poor_coverage"],
                "good_coverage": stats["good_coverage"],
                "total": stats["no_coverage"] + stats["poor_coverage"] + stats["good_coverage"]
            }
            for cat, stats in category_stats.items()
        }
    }
    
    output_data = {
        "metadata": {
            "timestamp": get_timestamp(),
            "total_questions": total_questions,
            "total_notes": stats['total_notes'],
            "very_low_threshold": VERY_LOW_THRESHOLD,
            "confidence_threshold": CONFIDENCE_THRESHOLD
        },
        "summary": summary,
        "gaps": {
            "no_coverage": no_coverage,
            "poor_coverage": poor_coverage,
            "good_coverage": good_coverage
        },
        "gap_categories": {
            cat: {
                "no_coverage": [r for r in results if r["category"] == cat and r["coverage"] == "no_coverage"],
                "poor_coverage": [r for r in results if r["category"] == cat and r["coverage"] == "poor_coverage"],
                "good_coverage": [r for r in results if r["category"] == cat and r["coverage"] == "good_coverage"]
            }
            for cat in RECRUITER_QUESTIONS.keys()
        }
    }
    
    results_dir = Path(__file__).parent.parent / "test-results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = get_timestamp()
    output_file = results_dir / f"gap-analysis-100-questions-{timestamp}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    print(f"\nTotal Questions: {total_questions}")
    print(f"No Coverage: {summary['no_coverage']} ({summary['no_coverage']/total_questions*100:.1f}%)")
    print(f"Poor Coverage: {summary['poor_coverage']} ({summary['poor_coverage']/total_questions*100:.1f}%)")
    print(f"Good Coverage: {summary['good_coverage']} ({summary['good_coverage']/total_questions*100:.1f}%)")
    
    print("\nBy Category:")
    for category, stats in summary['by_category'].items():
        print(f"\n  {category}:")
        print(f"    No Coverage: {stats['no_coverage']}/{stats['total']}")
        print(f"    Poor Coverage: {stats['poor_coverage']}/{stats['total']}")
        print(f"    Good Coverage: {stats['good_coverage']}/{stats['total']}")
    
    print(f"\n✅ Results saved to: {output_file}")
    print("=" * 80)
    
    print("\n⚠️  GAP ANALYSIS - Questions Needing Better Coverage:")
    print("=" * 80)
    
    if no_coverage:
        print(f"\nNO COVERAGE ({len(no_coverage)} questions):")
        for r in no_coverage[:10]:
            print(f"  - [{r['category']}] {r['question']} (score: {r['top_score']:.4f})")
        if len(no_coverage) > 10:
            print(f"  ... and {len(no_coverage) - 10} more")
    
    if poor_coverage:
        print(f"\nPOOR COVERAGE ({len(poor_coverage)} questions):")
        for r in poor_coverage[:10]:
            print(f"  - [{r['category']}] {r['question']} (score: {r['top_score']:.4f})")
        if len(poor_coverage) > 10:
            print(f"  ... and {len(poor_coverage) - 10} more")

if __name__ == "__main__":
    main()

