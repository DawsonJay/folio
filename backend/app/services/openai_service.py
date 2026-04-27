import os
import json
from typing import List, Dict, Optional, Any
from openai import OpenAI

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-4o-mini"
        
        self.valid_emotions = ["happy", "thinking", "surprised", "derp", "tired", "annoyed"]
        self.default_emotion = "happy"
    
    def get_embedding(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=texts
        )
        return [item.embedding for item in response.data]
    
    def match_direct_answer_title(
        self, question: str, candidate_titles: List[str]
    ) -> Dict[str, Any]:
        if not candidate_titles:
            return {"title": None, "confidence": 0.0}
        allowed = set(candidate_titles)
        list_block = "\n".join(f"- {t}" for t in candidate_titles)
        system_message = (
            "You map user questions to at most one pre-written question title from a closed list.\n"
            'Return JSON only: {"title": <string or null>, "confidence": <number 0-1>}\n'
            "Rules:\n"
            '- "title" must be EXACTLY one of the list strings below, character-for-character, or null.\n'
            "- If the user is asking the same thing as a title (including casual phrasing), pick that title.\n"
            "- If none match strongly, set title to null and confidence to 0.0-0.3.\n"
            "- confidence: how well the user question and the selected title are semantically the same ask."
        )
        user_message = f"User question:\n{question}\n\nAllowed titles (choose one exactly or null):\n{list_block}"
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.1,
            max_tokens=64,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        title = result.get("title")
        conf_raw = result.get("confidence", 0.0)
        try:
            conf = float(conf_raw)
        except (TypeError, ValueError):
            conf = 0.0
        conf = max(0.0, min(1.0, conf))
        if title in (None, ""):
            return {"title": None, "confidence": conf}
        if not isinstance(title, str):
            return {"title": None, "confidence": 0.0}
        if title not in allowed:
            return {"title": None, "confidence": 0.0}
        return {"title": title, "confidence": conf}
    
    def generate_chat_response(
        self,
        question: str,
        context: str,
        suggestion_list: str = "",
        project_links: Optional[Dict[str, Dict[str, str]]] = None,
        qualification: Optional[str] = None
    ) -> dict:
        project_links_json = json.dumps(project_links) if project_links else "{}"
        
        system_message = """Answer AS James (1st person ALWAYS). When asked about Folio project, acknowledge "I am Folio, the AI chatbot you're talking to right now" + AI/RAG aspect. Otherwise, never mention Folio.

CRITICAL - ACCURACY FIRST:
- Use ONLY facts from context. NEVER invent project descriptions, technologies, or details.
- If context says "Atlantis is a lake bed mapping system" - use EXACTLY that, not "AI assistant" or other inventions.
- If context says "Cirrus is a weather prediction system" - use EXACTLY that, not "cloud data management".
- Portfolio accuracy is ESSENTIAL. Invented facts destroy credibility.

WORD COUNTS (ADAPTIVE TO CONTEXT - CRITICAL):
- Minimum: 150 words (always meet this, even with sparse context)
- Maximum: 400 words (never exceed this)
- CRITICAL: Assess context richness FIRST, then write to match:
  * Rich context (multiple detailed notes, comprehensive coverage, extensive technical details): 300-400 words - USE THE DETAILS PROVIDED
  * Moderate context (some relevant notes, decent detail): 200-300 words
  * Sparse context (limited notes, basic info only): 150-200 words
- DO NOT default to brevity. If context provides detailed project stories, technical challenges, multiple examples, or comprehensive background - write 300-400 words using that richness.
- If you see context with problem descriptions, solution evolutions, lessons learned, or multiple project details - that's RICH context requiring 300-400 words.
- Err on the side of using MORE context rather than summarizing. Recruiters want substantial, detailed answers when information is available.

FORMATTING:
- Recruiter-friendly, explain tech briefly.
- Plain text ONLY. NO markdown: no **, no *, no _, no -, no 1., no [](). NO raw URLs in text (projectLinks handle that). Natural paragraphs.

PRONOUNS (CRITICAL):
- Personal projects (Atlantis, Cirrus, WhatNow, moh-ami, Folio, Jam Hot): "I built", "I developed", "my project" - NEVER neutral "Atlantis is"
- Work (Nurtur/BriefYourMarket): "I" for solo, "we" for team
- Example: "I built Atlantis, an ongoing project..." NOT "Atlantis is a project..."

EMPLOYMENT STATUS (CRITICAL - CURRENTLY UNEMPLOYED):
- CURRENT STATUS: I am currently UNEMPLOYED. I am NOT currently employed anywhere.
- Nurtur employment ended in February 2026 (redundancy). The redundancy process is COMPLETE. I am no longer at Nurtur.
- When asked "current employment status", "are you currently employed", or "where do you work": ALWAYS state "I am currently unemployed. I was made redundant at Nurtur in February 2026 and I am now actively seeking new opportunities. I am ready to start immediately."
- NEVER say "I am currently employed", "I work at Nurtur", "I am navigating the redundancy process", or "I'm in the redundancy process" - these are all WRONG
- ALWAYS use PAST TENSE when describing Nurtur work: "I worked at Nurtur", "I was a Full Stack Developer at Nurtur", "I built systems at Nurtur"
- Duration: "3.5 years" or "three and a half years" (NOT "2+ years")
- Example for current status: "I am currently unemployed. I worked at Nurtur for 3.5 years (July 2022 - February 2026) until I was made redundant. I am ready to start a new role immediately."

PROJECT STATUS (ALWAYS EXPLICIT):
- State clearly: "ongoing project" / "completed project" / "cancelled project"
- Example: "I developed WhatNow, a completed project..." NOT just "I developed WhatNow"

JSON: {"answer":"","emotion":"happy|thinking|surprised|derp","suggestions":[{"text":""}×6],"projectLinks":{"Name":{"demo":"","github":""}}}

Emotion: happy (positive) / thinking (technical) / surprised (impressive) / derp (limitations)
Suggestions: Choose exactly 6 from the SUGGESTION LIST provided in the user message. Pick the 6 most relevant to the answer just given. Use the EXACT text from the list — do not alter, abbreviate, or invent new suggestions."""

        qualification_prefix = f'\n\nStart: "{qualification}"' if qualification else ""
        
        user_message = f"""Context:
{context}

Links: {project_links_json}

Q: {question}{qualification_prefix}

Write a detailed answer using the context provided. Assess context richness: if context has multiple detailed notes, technical challenges, project stories, or comprehensive information, write 300-400 words. If moderate detail, write 200-300 words. If sparse, write 150-200 words minimum. Use the available context - don't summarize everything into a brief answer. Include links if relevant.

Choose exactly 6 suggestions from the SUGGESTION LIST below. Pick the ones most relevant to the answer just given. Use the EXACT text from the list. JSON only.

SUGGESTION LIST:
{suggestion_list}"""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        if result.get("emotion") not in self.valid_emotions:
            result["emotion"] = self.default_emotion
        
        if not isinstance(result.get("suggestions"), list):
            result["suggestions"] = []
        
        fallbacks = [
            "Tell me about yourself",
            "What are your strongest technical skills?",
            "What projects have you built?",
            "Why are you looking for a new role?",
            "What is Folio?",
            "What are you looking for in your next role?",
        ]
        i = 0
        while len(result["suggestions"]) < 6:
            result["suggestions"].append({"text": fallbacks[i % len(fallbacks)]})
            i += 1
        
        return result
    
    def generate_redirect_response(self, question: str, weak_context: str, suggestion_list: str = "") -> dict:
        system_message = """Answer AS James (1st person ALWAYS). Mention Folio only if asked about Folio project.

CRITICAL: Use ONLY facts from context. NEVER invent project descriptions or details.

When context is available, provide a helpful answer using that context. If context is truly insufficient, acknowledge limits and suggest alternatives.
- If context has relevant information, use it to answer the question (150-300 words)
- If context is truly insufficient, acknowledge limits (100-150 words)
- Plain text ONLY. NO markdown: no **, no *, no _, no -, no [](). NO raw URLs.

PRONOUNS: Personal projects (Atlantis, Cirrus, WhatNow, moh-ami, Folio, Jam Hot)="I built/developed" NOT neutral. Work="I" solo, "we" team.
STATUS: If mention projects, state "ongoing"/"completed"/"cancelled" explicitly.

JSON: {"answer":"","emotion":"thinking|derp","suggestions":[{"text":""}×6]}

Suggestions: Choose exactly 6 from the SUGGESTION LIST provided in the user message. Use the EXACT text from the list — do not alter, abbreviate, or invent new suggestions."""

        user_message = f"""Q: {question}

Context: {weak_context}

Answer the question using the context provided. If the context contains relevant information, provide a detailed answer (150-300 words). If context is truly insufficient, acknowledge that. Choose exactly 6 suggestions from the SUGGESTION LIST below. Use the EXACT text from the list. JSON only.

SUGGESTION LIST:
{suggestion_list}"""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        if result.get("emotion") not in ["thinking", "derp"]:
            result["emotion"] = "thinking"
        
        if not isinstance(result.get("suggestions"), list):
            result["suggestions"] = []
        
        fallbacks = [
            "Tell me about yourself",
            "What are your strongest technical skills?",
            "What projects have you built?",
            "Why are you looking for a new role?",
            "What is Folio?",
            "What are you looking for in your next role?",
        ]
        i = 0
        while len(result["suggestions"]) < 6:
            result["suggestions"].append({"text": fallbacks[i % len(fallbacks)]})
            i += 1
        
        return result
    
    def generate_off_topic_response(self) -> dict:
        return {
            "answer": "That seems outside the scope of my portfolio knowledge base. I'm here to answer questions about James's professional experience, technical skills, and project work.\n\nWhat would you like to know about his development experience, projects, or technical approach?",
            "emotion": "thinking",
            "suggestions": [
                {"text": "Tell me about yourself"},
                {"text": "What are your strongest technical skills?"},
                {"text": "What projects have you built?"},
                {"text": "Why are you looking for a new role?"},
                {"text": "How do you approach problem-solving?"},
                {"text": "How did you transition from art to tech?"}
            ]
        }
    
    def generate_boundary_response(self) -> dict:
        return {
            "answer": "I'm here to help you learn about James's professional background and experience. Please keep questions professional and on-topic.\n\nIf you're interested in James's work, I'd be happy to answer questions about his technical skills, projects, or development approach.",
            "emotion": "annoyed",
            "suggestions": [
                {"text": "What is Folio?"},
                {"text": "What's your experience with RAG systems?"},
                {"text": "Do you have experience with LLMs?"},
                {"text": "What AI/ML experience do you have?"},
                {"text": "What are your strongest technical skills?"},
                {"text": "Tell me about yourself"}
            ]
        }

