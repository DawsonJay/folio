"""
Test script: Canadian Tech Recruiter Interview
Role: Frontend/Full-Stack Developer (React/TypeScript)
Company: Small-mid size, hybrid (2 days/week in office)
Salary: ~100K CAD
"""

import requests
import json
import time
from datetime import datetime

API_URL = "http://localhost:8000/api/chat"

# 20 recruiter questions from a Canadian tech company hiring mid-level React/TypeScript developer
QUESTIONS = [
    # Opening questions
    "Tell me about yourself",
    "Walk me through your experience with React and TypeScript",
    "Why are you looking to move to Canada?",
    
    # Technical depth
    "What's your experience with state management? Redux, Context, etc?",
    "Tell me about a complex technical problem you've solved",
    "How do you approach performance optimization?",
    "What's your testing strategy?",
    
    # Work experience  
    "Tell me about your role at Nurtur",
    "What was your biggest accomplishment there?",
    "Have you led any projects?",
    "How did you work with backend developers?",
    
    # Team fit
    "What size team do you prefer working in?",
    "Tell me about a time you mentored someone",
    "How do you handle code reviews?",
    
    # AI/ML angle (since they see it on resume)
    "I see you have AI/ML experience - tell me about that",
    "Have you integrated AI into web applications?",
    
    # Practical logistics
    "What's your visa status for Canada?",
    "When can you start?",
    "Are you okay with hybrid work - 2 days in office?",
    
    # Closing
    "What are your salary expectations?"
]

def ask_question(question, session_id):
    """Ask a question to the chatbot API"""
    try:
        response = requests.post(
            API_URL,
            json={"question": question, "session_id": session_id},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return {
            "question": question,
            "answer": data.get("answer", ""),
            "confidence": data.get("confidence", ""),
            "score": data.get("top_score", 0),
            "response_time": 0  # Not in response
        }
    except Exception as e:
        return {
            "question": question,
            "answer": f"ERROR: {str(e)}",
            "confidence": "error",
            "score": 0,
            "response_time": 0
        }

def rate_answer(question, answer, context):
    """Rate answer from recruiter perspective (1-5 scale)"""
    # This is a simple heuristic - you can make it more sophisticated
    rating = {
        "relevance": 0,
        "clarity": 0,
        "credibility": 0,
        "fit": 0,
        "concerns": []
    }
    
    answer_lower = answer.lower()
    
    # Check for positive signals
    if "3+ years" in answer or "zero maintenance" in answer:
        rating["credibility"] += 1
    if "mentored" in answer_lower or "leadership" in answer_lower:
        rating["fit"] += 1
    if "react" in answer_lower and "typescript" in answer_lower:
        rating["relevance"] += 1
    if len(answer) > 100 and len(answer) < 2000:
        rating["clarity"] += 1
    
    # Check for red flags
    if "junior" in answer_lower and "title" in answer_lower:
        rating["concerns"].append("Mentions title discrepancy")
    if "solo" in answer_lower and "integrations" in answer_lower:
        rating["concerns"].append("Claims solo on Integrations")
    if "ego" in answer_lower or "pretension" in answer_lower:
        rating["concerns"].append("Negative language about previous environment")
    if len(answer) > 2500:
        rating["concerns"].append("Too long - loses attention")
        
    return rating

def main():
    print("=" * 80)
    print("RECRUITER INTERVIEW TEST")
    print("=" * 80)
    print(f"Company: Small Canadian tech company (50 people)")
    print(f"Role: Frontend/Full-Stack Developer (React/TypeScript)")
    print(f"Level: Mid-level")
    print(f"Salary: ~$100K CAD")
    print(f"Work: Hybrid (2 days/week in office)")
    print("=" * 80)
    print()
    
    session_id = f"recruiter-test-{int(time.time())}"
    results = []
    
    for i, question in enumerate(QUESTIONS, 1):
        print(f"\n[Q{i}/20] {question}")
        print("-" * 80)
        
        result = ask_question(question, session_id)
        rating = rate_answer(question, result["answer"], "canadian_recruiter")
        
        result["rating"] = rating
        results.append(result)
        
        # Print shortened answer
        answer = result["answer"]
        if len(answer) > 500:
            print(f"{answer[:500]}...")
        else:
            print(answer)
            
        print(f"\nConfidence: {result['confidence']} | Score: {result['score']:.3f}")
        
        if rating["concerns"]:
            print(f"[!] CONCERNS: {', '.join(rating['concerns'])}")
        
        time.sleep(0.5)  # Be nice to the API
    
    # Generate summary
    print("\n" + "=" * 80)
    print("INTERVIEW SUMMARY")
    print("=" * 80)
    
    total_concerns = sum(len(r["rating"]["concerns"]) for r in results)
    avg_score = sum(r["score"] for r in results) / len(results)
    
    print(f"\nTotal Questions: {len(results)}")
    print(f"Average Confidence Score: {avg_score:.3f}")
    print(f"Total Red Flags: {total_concerns}")
    
    if total_concerns > 0:
        print(f"\n[!] RED FLAGS FOUND:")
        for i, result in enumerate(results, 1):
            if result["rating"]["concerns"]:
                print(f"  Q{i}: {result['question']}")
                for concern in result["rating"]["concerns"]:
                    print(f"    - {concern}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recruiter_interview_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n[OK] Results saved to: {filename}")
    
    # Overall assessment
    print("\n" + "=" * 80)
    print("RECRUITER VERDICT")
    print("=" * 80)
    
    if total_concerns == 0 and avg_score > 0.7:
        print("[STRONG] STRONG CANDIDATE - Would move to next round")
    elif total_concerns <= 2 and avg_score > 0.6:
        print("[SOLID] SOLID CANDIDATE - Would interview")
    elif total_concerns <= 5:
        print("[MAYBE] MAYBE - Has concerns but might work")
    else:
        print("[PASS] PASS - Too many red flags")

if __name__ == "__main__":
    main()
