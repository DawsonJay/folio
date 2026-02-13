# Direct Answer Quality Test Specification

## Purpose
Validate that tier-1 direct answers are high quality and frame the candidate well to recruiters. Tests both **retrieval** (right answer found) and **content** (answer meets gold standard).

---

## Test Categories & Questions

### 1. Opening (must nail these)
- Tell me about yourself
- Walk me through your experience with React and TypeScript
- Why are you looking for a new role?
- Why should we hire you?

### 2. Work Experience & Accomplishments
- Tell me about your role at Nurtur
- What was your biggest accomplishment at Nurtur?
- What was your biggest accomplishment there?
- Have you led any projects?
- How did you grow in your position at Nurtur?
- Tell me about your most recent role
- What did you do at Nurtur?

### 3. Technical Depth
- What's your experience with state management? Redux, Context?
- Tell me about a complex technical problem you've solved
- How do you approach performance optimization?
- What's your testing strategy?
- How do you make technical decisions?
- What's your debugging process?

### 4. Team & Collaboration
- What size team do you prefer?
- Tell me about a time you mentored someone
- How do you handle code reviews?
- How do you work with backend developers?
- How do you handle conflict in teams?

### 5. AI/ML (differentiator)
- I see you have AI/ML experience - tell me about that
- Have you integrated AI into web applications?
- What AI/ML experience do you have?

### 6. Logistics & Practicals
- What's your visa status for Canada?
- When can you start?
- Are you okay with hybrid work - 2 days in office?
- Are you comfortable with hybrid work?
- Are you open to remote work?
- What are your salary expectations?
- What's your current employment status?

### 7. Canada / Relocation (if applicable)
- Why are you looking to move to Canada?
- Why Canada?
- How will you handle the transition period to Canada?

### 8. Behavioral / Softer
- What are your strengths?
- What's your biggest weakness?
- How do you handle failure?
- Tell me about a mistake you made
- What are you looking for in your next role?

### 9. Edge / Consistency checks
- What project are you most proud of?
- What's your favorite project?
- Which project best demonstrates your skills?

---

## Quality Criteria (Gold Standard)

### Retrieval
- **Critical questions** (opening, salary, start date, hybrid, remote, biggest accomplishment): must return `direct_answer` with score >= 0.65.
- **Overall direct answer rate**: >= 70% of questions should hit a direct answer (not synthesized/RAG).

### Content – Red Flags (fail if present)
- **Prescriptive language**: "This demonstrates...", "This proves...", "What makes me unique...", "My superpower..."
- **Junior / title**: Any mention of "junior" (except in growth context e.g. "from bootcamp to...")
- **Integrations overclaim**: "solo" + "Integrations" (should be "sole frontend" / "learned backend under mentorship")
- **Negative framing**: "ego", "pretension", "question is a little vague", "I am currently unemployed" as opener
- **Salary dodge**: Salary question answered without any number or range (£ or $)
- **Too long**: > 350 words (loses recruiter attention)
- **Too short / generic**: < 60 words and no concrete project names or metrics

### Content – Positive Signals (should see where relevant)
- **Credibility anchors**: "3+ years", "zero maintenance", concrete project names (Integrations Dashboard, Nexus, WhatNow)
- **Metrics**: numbers (15+ seconds to under 5, 15+ users, 3 backend developers mentored)
- **Direct answer**: Opens with fact or "Yes/Absolutely" + proof, not "The question is..."
- **Nexus**: When leadership discussed, "technical lead" not just "worked on"
- **Integrations**: When ownership discussed, "sole frontend" and/or "learned backend under mentorship"

### Length (guidance, not hard fail)
- Tier 1 (tell me about yourself, why hire you): 150–250 words
- Tier 2 (technical): 100–200 words
- Tier 3 (behavioral/specific): 80–150 words
- Flag if < 80 or > 300 for standard questions

---

## Output
- **Per question**: question, category, confidence, score, word_count, used_direct_answer (Y/N), pass/fail, red_flags[], positive_signals[], length_ok
- **Summary**: total_questions, direct_answer_count, direct_answer_rate, critical_pass_count, critical_fail_count, total_red_flags, overall_grade (A/B/C/F)
- **Report file**: `direct-answer-quality-report-{timestamp}.md` with full details and list of fixes needed
