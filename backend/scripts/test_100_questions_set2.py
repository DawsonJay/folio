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

# NEW SET OF 100 INTERVIEW QUESTIONS (Different from Set 1)
INTERVIEW_QUESTIONS_SET2 = {
    "Technical Skills & Experience": [
        "Walk me through your technical stack",
        "What's your strongest programming language?",
        "How do you approach learning a new framework?",
        "Tell me about a recent technical challenge",
        "What development tools do you use daily?",
        "How do you ensure code quality?",
        "What's your experience with version control?",
        "Describe your testing approach",
        "How comfortable are you with backend development?",
        "What frontend frameworks have you worked with?",
    ],
    
    "AI/ML & Emerging Tech": [
        "How have you used AI in your projects?",
        "What's your experience with machine learning?",
        "Have you integrated LLMs into applications?",
        "Tell me about working with embeddings",
        "What AI tools or APIs have you used?",
        "How do you see AI changing web development?",
        "What's your understanding of RAG systems?",
        "Have you worked with recommendation engines?",
        "What ML frameworks are you familiar with?",
        "How do you approach AI project requirements?",
    ],
    
    "Project & Portfolio": [
        "Walk me through your portfolio",
        "What's your most impressive project?",
        "Tell me about a project you're proud of",
        "What was the biggest project you led?",
        "How do you choose what to build?",
        "What's a project that didn't go as planned?",
        "How do you validate project ideas?",
        "What's the longest-running project you've maintained?",
        "Tell me about a time you rescued a failing project",
        "How do you measure project success?",
    ],
    
    "Problem Solving & Debugging": [
        "How do you approach a new technical problem?",
        "Walk me through your debugging process",
        "Tell me about a time you solved a critical bug",
        "How do you handle production issues?",
        "What's your process for troubleshooting?",
        "How do you deal with unclear error messages?",
        "Tell me about investigating a performance issue",
        "How do you prevent bugs in the first place?",
        "What's your approach to code review?",
        "How do you balance fixing bugs vs building features?",
    ],
    
    "Team & Communication": [
        "How do you collaborate with other developers?",
        "Tell me about working with designers",
        "How do you handle difficult teammates?",
        "What's your communication style?",
        "How do you give constructive feedback?",
        "Tell me about mentoring junior developers",
        "How do you resolve technical disagreements?",
        "What makes you a good teammate?",
        "How do you keep stakeholders informed?",
        "Tell me about pair programming experience",
    ],
    
    "Leadership & Initiative": [
        "Have you led any projects?",
        "How do you take initiative on a team?",
        "Tell me about influencing technical decisions",
        "How do you handle project ownership?",
        "What's your approach to delegating work?",
        "How do you motivate team members?",
        "Tell me about a time you stepped up as a leader",
        "How do you handle responsibility?",
        "What's your leadership philosophy?",
        "How do you build trust with your team?",
    ],
    
    "Work Style & Productivity": [
        "How do you manage your time?",
        "What's your typical day like?",
        "How do you handle multiple priorities?",
        "What makes you productive?",
        "How do you avoid burnout?",
        "What's your preferred work environment?",
        "How do you stay focused?",
        "What's your approach to deadlines?",
        "How do you handle interruptions?",
        "What tools help you stay organized?",
    ],
    
    "Professional Development": [
        "How do you keep your skills current?",
        "What are you currently learning?",
        "How do you evaluate new technologies?",
        "What conferences or resources do you follow?",
        "How do you decide what to learn next?",
        "Tell me about your learning process",
        "What technical blogs do you read?",
        "How do you share knowledge with others?",
        "What certifications do you have?",
        "How do you track industry trends?",
    ],
    
    "Career & Motivation": [
        "What attracted you to this position?",
        "Why are you leaving your current job?",
        "What are you looking for in your next role?",
        "What type of projects excite you?",
        "How do you define career success?",
        "What impact do you want to make?",
        "What kind of company culture do you prefer?",
        "What are your salary expectations?",
        "Why did you choose software development?",
        "What's most important to you in a job?",
    ],
    
    "Behavioral & Soft Skills": [
        "Tell me about a time you failed",
        "How do you handle criticism?",
        "Describe a difficult decision you made",
        "How do you deal with ambiguity?",
        "Tell me about a conflict you resolved",
        "How do you handle tight deadlines?",
        "What's your approach to work-life balance?",
        "How do you adapt to change?",
        "Tell me about receiving difficult feedback",
        "How do you build relationships at work?",
    ],
}

ALL_QUESTIONS = []
for category, questions in INTERVIEW_QUESTIONS_SET2.items():
    for question in questions:
        ALL_QUESTIONS.append({
            "category": category,
            "question": question
        })

def evaluate_retrieval(question, notes_retrieved, category):
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
    print("INTERVIEW TEST SET 2 - 100 NEW QUESTIONS")
    print("="*80)
    print("\nInitializing services...")
    openai_service = OpenAIService()
    embedding_storage = LocalEmbeddingStorage(storage_path=str(EMBEDDINGS_FILE))

    stats = embedding_storage.get_stats()
    if stats['total_notes'] == 0:
        print(f"Error: No embeddings found.")
        sys.exit(1)
    
    print(f"Loaded {stats['total_notes']} notes from storage")
    print(f"Testing {len(ALL_QUESTIONS)} questions across {len(INTERVIEW_QUESTIONS_SET2)} categories\n")
    
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
    print("SUMMARY REPORT - SET 2")
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
        print(f"\nFound {len(gaps)} questions with adequate or weak coverage:\n")
        weak_only = [g for g in gaps if g['quality_score'] <= 2]
        if weak_only:
            print(f"WEAK/POOR ({len(weak_only)}):")
            for gap in weak_only[:20]:
                print(f"  [{gap['quality_score']}/5] {gap['question']}")
                print(f"          Top note: {gap['top_notes'][0] if gap['top_notes'] else 'None'} ({gap['top_scores'][0]:.3f})")
        else:
            print("  ✅ No weak/poor scores!")
            print(f"\n  Most adequate scores are usable (top similarity > 0.35)")
    else:
        print("\n  🎉 No gaps found! All questions have good coverage.")
    
    output_file = Path(__file__).parent.parent / "TEST-RESULTS-SET2.json"
    with open(output_file, 'w') as f:
        json.dump({
            "test_name": "Interview Questions Set 2",
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
    print("COMPARISON WITH SET 1")
    print("="*80)
    
    # Try to load Set 1 results for comparison
    set1_file = Path(__file__).parent.parent / "TEST-RESULTS-100-QUESTIONS.json"
    if set1_file.exists():
        with open(set1_file, 'r') as f:
            set1_data = json.load(f)
        
        print(f"\nSet 1 Score: {set1_data['overall_score']:.2f}/5.0")
        print(f"Set 2 Score: {overall_avg:.2f}/5.0")
        print(f"Difference: {overall_avg - set1_data['overall_score']:+.2f}")
        
        print(f"\nSet 1 Weak/Poor: {set1_data['score_distribution'].get('2', 0) + set1_data['score_distribution'].get('1', 0)}%")
        print(f"Set 2 Weak/Poor: {score_dist[2] + score_dist[1]}%")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()

