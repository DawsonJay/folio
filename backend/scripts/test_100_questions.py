import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

sys.path.append(str(Path(__file__).parent.parent))

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage

load_dotenv()

EMBEDDINGS_FILE = Path(__file__).parent.parent / "embeddings.json"

INTERVIEW_QUESTIONS = {
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
    
    "Project Deep Dives": [
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
    ],
    
    "Technical Challenges": [
        "Tell me about a difficult technical problem you solved",
        "What was your biggest technical challenge?",
        "How do you debug complex issues?",
        "Tell me about a time you had to learn something quickly",
        "How do you handle technical debt?",
        "What's the hardest bug you've fixed?",
        "Tell me about optimizing performance",
        "How do you approach system architecture?",
        "Tell me about scaling a system",
        "What's a technical decision you regret?",
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
    
    "Problem Solving": [
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
    
    "Career & Growth": [
        "Why do you want to work in Canada?",
        "What are your career goals?",
        "Why are you interested in this role?",
        "What are you learning right now?",
        "Where do you see yourself in 5 years?",
        "Why did you transition from theatre to tech?",
        "Tell me about your educational background",
        "What drives you as a developer?",
        "What areas do you want to grow in?",
        "Why should we hire you?",
    ],
    
    "Soft Skills & Values": [
        "What are your core values?",
        "How do you handle stress?",
        "What motivates you?",
        "How do you handle feedback?",
        "What's your work style?",
        "How do you maintain work-life balance?",
        "What makes you passionate about coding?",
        "How do you stay current with technology?",
        "What's your ideal work environment?",
        "How do you handle failure?",
    ],
    
    "Specific Technologies": [
        "Tell me about your Redux experience",
        "What's your experience with state management?",
        "Have you used Lexical framework?",
        "Tell me about working with embeddings",
        "What's your experience with PostgreSQL?",
        "Have you used Prisma?",
        "Tell me about Next.js experience",
        "What CSS frameworks do you know?",
        "Have you worked with FastAPI?",
        "Tell me about your Docker experience",
    ],
}

ALL_QUESTIONS = []
for category, questions in INTERVIEW_QUESTIONS.items():
    for question in questions:
        ALL_QUESTIONS.append({
            "category": category,
            "question": question
        })

def evaluate_retrieval(question, notes_retrieved, category):
    """
    Evaluate if retrieved notes are appropriate for the question.
    """
    note_titles = [note['id'] for note in notes_retrieved]
    note_scores = [note['score'] for note in notes_retrieved]
    
    relevant_count = sum(1 for score in note_scores if score > 0.4)
    top_score = note_scores[0] if note_scores else 0
    
    if top_score > 0.5 and relevant_count >= 3:
        quality = "Excellent"
        score = 5
    elif top_score > 0.45 and relevant_count >= 2:
        quality = "Good"
        score = 4
    elif top_score > 0.35 and relevant_count >= 1:
        quality = "Adequate"
        score = 3
    elif top_score > 0.25:
        quality = "Weak"
        score = 2
    else:
        quality = "Poor"
        score = 1
    
    return score, quality, note_titles, note_scores

def main():
    print("="*80)
    print("COMPREHENSIVE 100-QUESTION INTERVIEW TEST")
    print("="*80)
    print("\nInitializing services...")
    openai_service = OpenAIService()
    embedding_storage = LocalEmbeddingStorage(storage_path=str(EMBEDDINGS_FILE))

    stats = embedding_storage.get_stats()
    if stats['total_notes'] == 0:
        print(f"Error: No embeddings found.")
        sys.exit(1)
    
    print(f"Loaded {stats['total_notes']} notes from storage")
    print(f"Testing {len(ALL_QUESTIONS)} questions across {len(INTERVIEW_QUESTIONS)} categories\n")
    
    results = []
    category_scores = {}
    
    for i, item in enumerate(ALL_QUESTIONS, 1):
        question = item['question']
        category = item['category']
        
        print(f"[{i:3d}/100] {question[:60]}{'...' if len(question) > 60 else ''}")
        
        query_embedding = openai_service.get_embedding(question)
        similar_notes = embedding_storage.query_similar(query_embedding, top_k=5)
        
        score, quality, note_titles, note_scores = evaluate_retrieval(question, similar_notes, category)
        
        print(f"          → {quality} ({score}/5) | Top: {note_titles[0][:40] if note_titles else 'None'} ({note_scores[0]:.3f})")
        
        result = {
            "question": question,
            "category": category,
            "quality_score": score,
            "quality": quality,
            "top_notes": note_titles[:3],
            "top_scores": note_scores[:3]
        }
        results.append(result)
        
        if category not in category_scores:
            category_scores[category] = []
        category_scores[category].append(score)
    
    print("\n" + "="*80)
    print("SUMMARY REPORT")
    print("="*80)
    
    overall_avg = sum(r['quality_score'] for r in results) / len(results)
    print(f"\n📊 Overall Average Score: {overall_avg:.2f}/5.0")
    
    score_dist = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for r in results:
        score_dist[r['quality_score']] += 1
    
    print(f"\n📈 Score Distribution:")
    print(f"   Excellent (5): {score_dist[5]}/100 ({score_dist[5]}%)")
    print(f"   Good (4):      {score_dist[4]}/100 ({score_dist[4]}%)")
    print(f"   Adequate (3):  {score_dist[3]}/100 ({score_dist[3]}%)")
    print(f"   Weak (2):      {score_dist[2]}/100 ({score_dist[2]}%)")
    print(f"   Poor (1):      {score_dist[1]}/100 ({score_dist[1]}%)")
    
    print("\n" + "-"*80)
    print("CATEGORY BREAKDOWN")
    print("-"*80)
    
    for category, scores in sorted(category_scores.items(), key=lambda x: -sum(x[1])/len(x[1])):
        avg = sum(scores) / len(scores)
        excellent = sum(1 for s in scores if s == 5)
        good = sum(1 for s in scores if s == 4)
        adequate = sum(1 for s in scores if s == 3)
        weak = sum(1 for s in scores if s <= 2)
        
        print(f"\n{category}:")
        print(f"  Average: {avg:.2f}/5.0 | E:{excellent} G:{good} A:{adequate} W:{weak}")
    
    print("\n" + "-"*80)
    print("COVERAGE GAPS (Questions scoring ≤3)")
    print("-"*80)
    
    gaps = [r for r in results if r['quality_score'] <= 3]
    if gaps:
        print(f"\nFound {len(gaps)} questions with weak coverage:\n")
        for gap in gaps[:15]:
            print(f"  [{gap['quality_score']}/5] {gap['question']}")
            print(f"          Category: {gap['category']}")
            print(f"          Top note: {gap['top_notes'][0] if gap['top_notes'] else 'None'} ({gap['top_scores'][0]:.3f})")
            print()
    else:
        print("\n  🎉 No significant gaps found! All questions have good coverage.")
    
    output_file = Path(__file__).parent.parent / "TEST-RESULTS-100-QUESTIONS.json"
    with open(output_file, 'w') as f:
        json.dump({
            "overall_score": overall_avg,
            "score_distribution": score_dist,
            "category_scores": {k: sum(v)/len(v) for k, v in category_scores.items()},
            "results": results,
            "gaps": gaps
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    if overall_avg >= 4.0:
        print("\n✅ EXCELLENT: System ready for production use!")
    elif overall_avg >= 3.5:
        print("\n✓ GOOD: System working well, minor improvements possible")
    elif overall_avg >= 3.0:
        print("\n⚠ ADEQUATE: System functional but needs more notes")
    else:
        print("\n❌ NEEDS WORK: Significant gaps in coverage")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()

