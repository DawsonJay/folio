# Prompt Gaps - LLM Prompt Design Issues

**Purpose:** Track prompt design issues that need fixing to improve recruiter-readiness  
**Created:** 2026-02-01  
**Status:** In Progress

## Critical Issues

### 1. Q1 Routing - "Tell me about yourself"
- [ ] **Issue:** Routes to redirect response instead of high-confidence answer
- [ ] **Current Behavior:** Returns "I can't provide specific details about you" - completely fails
- [ ] **Expected Behavior:** Should provide comprehensive self-introduction
- **Impact:** First impression completely fails - doesn't present James at all
- **Evidence:** Test result Q1: confidence="redirect", top_score=0.3648
- **Root Cause:** Confidence threshold too high OR embedding similarity too low for this question
- **Fix Required:**
  - Lower confidence threshold for "Tell me about yourself" OR
  - Add special handling for this common recruiter question OR
  - Improve note coverage/embedding for self-introduction content
- **Files to Update:** `backend/app/api/chat.py` (routing logic)

### 2. Generic Suggestions - Not Portfolio-Focused
- [ ] **Issue:** Q1 suggestions are all generic, not about James specifically
- [ ] **Current Suggestions:** "Key skills in tech", "Recent projects", "Favorite programming languages", etc.
- [ ] **Expected:** All suggestions should be about James, his work, experience, projects
- **Impact:** Suggests questions that could be asked of anyone, not portfolio-specific
- **Evidence:** Test result Q1 suggestions are completely generic
- **Fix Required:**
  - Update `generate_redirect_response()` prompt to require portfolio-focused suggestions
  - Add explicit instruction: "All suggestions must be about James, his work, experience, or projects - never generic questions"
- **Files to Update:** `backend/app/services/openai_service.py` (generate_redirect_response)

### 3. Project Context Missing in Answers
- [ ] **Issue:** Mentions project names (Atlantis, Cirrus, moh-ami) without brief context
- [ ] **Current Behavior:** "my project Cirrus" or "my work on Atlantis" - no explanation
- [ ] **Expected:** Brief one-sentence context when first mentioning a project
- **Impact:** Recruiters without tech knowledge won't understand what projects are
- **Evidence:** 
  - Q2: "Cirrus" mentioned without context
  - Q5: "Atlantis" mentioned without context  
  - Q10: "moh-ami" and "Cirrus" mentioned with minimal context
- **Fix Required:**
  - Update `generate_chat_response()` system message to include: "When mentioning projects, add brief context: 'Atlantis (a lake bed mapping system)' or 'Cirrus (a weather prediction system)'"
  - Ensure first mention of any project includes brief description
- **Files to Update:** `backend/app/services/openai_service.py` (generate_chat_response)

### 4. Problematic Suggestions - "What companies interest you?"
- [ ] **Issue:** Suggests questions that could reveal problematic answers
- [ ] **Current Behavior:** Q4 suggests "What companies interest you?"
- [ ] **Problem:** Honest answer would turn employers off (either "small teams/eco tech" OR "I'll work for anyone to immigrate")
- [ ] **Expected:** Never suggest company preference questions
- **Impact:** Could lead to answers that exclude James from consideration
- **Evidence:** Test result Q4 suggestion #3: "What companies interest you?"
- **Fix Required:**
  - Add to all prompt instructions: "NEVER suggest questions about company preferences, which companies interest the candidate, or similar questions that could reveal preferences that might turn employers away"
  - Update both `generate_chat_response()` and `generate_redirect_response()` prompts
- **Files to Update:** `backend/app/services/openai_service.py` (both methods)

## High Priority Issues

### 5. Suggestion Redundancy
- [ ] **Issue:** Same suggestions appear across multiple questions
- [ ] **Examples:**
  - Q3 and Q8: "What are your career goals?" (exact duplicate)
  - Q4 and Q3: "What skills do you want to develop?" (duplicate)
  - Q2 and Q5: "What projects have you worked on?" vs "Tell me about a project you're proud of" (similar intent)
  - Q6 and Q8: "What projects are you currently working on?" (exact duplicate)
- **Impact:** Reduces variety, makes suggestions less useful
- **Evidence:** Multiple duplicate suggestions across test results
- **Fix Required:**
  - Add instruction: "Ensure suggestions are unique and not redundant with previous suggestions"
  - Consider tracking recent suggestions to avoid immediate repeats
  - OR accept some redundancy as acceptable (verify with user)
- **Files to Update:** `backend/app/services/openai_service.py` (both generation methods)

### 6. Portfolio Focus Enforcement
- [ ] **Issue:** Some suggestions are generic rather than portfolio-focused
- [ ] **Current Behavior:** Mix of portfolio-focused and generic suggestions
- [ ] **Expected:** ALL suggestions must be about James, his work, experience, projects
- **Impact:** Generic suggestions don't showcase portfolio or lead to answerable questions
- **Evidence:** 
  - Q1: All generic
  - Q4: "What companies interest you?" (generic + problematic)
- **Fix Required:**
  - Strengthen instruction in all prompts: "ALL suggestions must be about James, his work, experience, skills, projects, or background - never generic questions that could apply to anyone"
  - Add examples of good vs bad suggestions
- **Files to Update:** `backend/app/services/openai_service.py` (all generation methods)

## Medium Priority Issues

### 7. Character Limit Verification
- [ ] **Issue:** Need to verify all suggestions respect 45-character limit
- [ ] **Current:** Limit is in prompt, but need to verify compliance
- **Evidence:** Most suggestions appear within limit, but should verify all
- **Fix Required:** 
  - Review test results for any suggestions exceeding 45 characters
  - If found, strengthen prompt instruction
- **Files to Update:** `backend/app/services/openai_service.py` (if needed)

### 8. Answer Quality for Non-Tech Recruiters
- [ ] **Issue:** Some answers assume tech knowledge
- [ ] **Current Behavior:** Uses technical terms without explanation
- [ ] **Expected:** Answers should be accessible to non-technical recruiters
- **Impact:** Recruiters may not understand answers fully
- **Evidence:** Some answers use technical jargon
- **Fix Required:**
  - Add instruction: "Write for non-technical recruiters - explain technical terms briefly when first used"
  - OR accept this as acceptable (verify with user)
- **Files to Update:** `backend/app/services/openai_service.py` (generate_chat_response)

## Summary

**Total Issues Identified:** 8  
**Critical:** 4  
**High Priority:** 2  
**Medium Priority:** 2

**Files Requiring Updates:**
- `backend/app/services/openai_service.py` (all generation methods)
- `backend/app/api/chat.py` (routing logic for Q1)

**Next Steps:**
1. Fix Q1 routing (critical)
2. Remove "What companies interest you?" suggestions (critical)
3. Add project context to answers (critical)
4. Enforce portfolio-focused suggestions (critical)
5. Address redundancy (high priority)
6. Verify character limits (medium priority)

