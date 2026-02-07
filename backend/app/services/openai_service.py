import os
import json
from typing import List, Dict, Optional
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
    
    def generate_chat_response(
        self, 
        question: str, 
        context: str,
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
Suggestions: 6 QUESTIONS (not statements) about James, max 45 char. BROAD/GENERAL questions about major portfolio topics (projects, skills, work experience, technical approach). NOT narrow/specific. Format: "What...", "How...", "Tell me about...". NEVER generic/company-preference questions."""

        qualification_prefix = f'\n\nStart: "{qualification}"' if qualification else ""
        
        user_message = f"""Context:
{context}

Links: {project_links_json}

Q: {question}{qualification_prefix}

Write a detailed answer using the context provided. Assess context richness: if context has multiple detailed notes, technical challenges, project stories, or comprehensive information, write 300-400 words. If moderate detail, write 200-300 words. If sparse, write 150-200 words minimum. Use the available context - don't summarize everything into a brief answer. Include links if relevant. 6 BROAD/GENERAL QUESTION suggestions about major portfolio topics (NOT narrow/specific questions). JSON only."""
        
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
        
        while len(result["suggestions"]) < 6:
            result["suggestions"].append({"text": f"Tell me more about that"})
        
        return result
    
    def generate_redirect_response(self, question: str, weak_context: str) -> dict:
        system_message = """Answer AS James (1st person ALWAYS). Mention Folio only if asked about Folio project.

CRITICAL: Use ONLY facts from context. NEVER invent project descriptions or details.

When context is available, provide a helpful answer using that context. If context is truly insufficient, acknowledge limits and suggest alternatives.
- If context has relevant information, use it to answer the question (150-300 words)
- If context is truly insufficient, acknowledge limits (100-150 words)
- Plain text ONLY. NO markdown: no **, no *, no _, no -, no [](). NO raw URLs.

PRONOUNS: Personal projects (Atlantis, Cirrus, WhatNow, moh-ami, Folio, Jam Hot)="I built/developed" NOT neutral. Work="I" solo, "we" team.
STATUS: If mention projects, state "ongoing"/"completed"/"cancelled" explicitly.

JSON: {"answer":"","emotion":"thinking|derp","suggestions":[{"text":""}×6]}

Suggestions: 6 QUESTIONS (not statements) about James, max 45 char. BROAD/GENERAL questions about major portfolio topics (projects, skills, work experience, technical approach). NOT narrow/specific. Format: "What...", "How...", "Tell me about...". NEVER generic/company-preference."""

        user_message = f"""Q: {question}

Context: {weak_context}

Answer the question using the context provided. If the context contains relevant information, provide a detailed answer (150-300 words). If context is truly insufficient, acknowledge that and suggest 6 BROAD/GENERAL QUESTION alternatives about James's major portfolio topics (projects, skills, work experience), max 45 char each. NOT narrow/specific. JSON only."""
        
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
        
        while len(result["suggestions"]) < 6:
            result["suggestions"].append({"text": "What projects have you built?"})
        
        return result
    
    def generate_off_topic_response(self) -> dict:
        return {
            "answer": "That seems outside the scope of my portfolio knowledge base. I'm here to answer questions about James's professional experience, technical skills, and project work.\n\nWhat would you like to know about his development experience, projects, or technical approach?",
            "emotion": "thinking",
            "suggestions": [
                {"text": "What projects have you built?"},
                {"text": "Tell me about your AI/ML work"},
                {"text": "What's your backend experience?"},
                {"text": "How do you approach debugging?"},
                {"text": "What's your frontend stack?"},
                {"text": "Tell me about your work process"}
            ]
        }
    
    def generate_boundary_response(self) -> dict:
        return {
            "answer": "I'm here to help you learn about James's professional background and experience. Please keep questions professional and on-topic.\n\nIf you're interested in James's work, I'd be happy to answer questions about his technical skills, projects, or development approach.",
            "emotion": "annoyed",
            "suggestions": [
                {"text": "What is Folio?"},
                {"text": "How does Folio work?"},
                {"text": "What tech powers Folio?"},
                {"text": "Why did you build Folio?"},
                {"text": "Tell me about the RAG system"},
                {"text": "How did you build Folio?"}
            ]
        }

