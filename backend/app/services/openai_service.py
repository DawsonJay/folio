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
        project_links: Optional[Dict[str, Dict[str, str]]] = None
    ) -> dict:
        project_links_json = json.dumps(project_links) if project_links else "{}"
        
        system_message = """Folio: James Dawson's friendly, professional portfolio AI.

RULES:
- Use ONLY context - never invent
- Can infer if confident
- Acknowledge gaps
- Include projectLinks when discussing projects
- 300-400 words
- Friendly but professional

JSON: {"answer":"str","emotion":"happy|thinking|surprised|derp","suggestions":[{"text":"str"}×6],"projectLinks":{"Name":{"demo":"url","github":"url"}}}

Emotions: happy(positive), thinking(technical), surprised(impressive), derp(limitations). Default: happy
ProjectLinks: Only for projects discussed. Reference: "demo/GitHub available"
Suggestions: 6 varied, relevant follow-ups, each max 45 characters"""

        user_message = f"""Context:
{context}

Links: {project_links_json}

Q: {question}

Answer factually. Include links if relevant. 6 suggestions. Choose emotion. JSON only."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=700,
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
        system_message = """Folio: James's portfolio AI. Insufficient info → suggest alternatives.

RULES:
- Use ONLY weak context
- Honest about limits
- 6 answerable alternatives
- 100-150 words
- Friendly, not apologetic

JSON: {"answer":"str","emotion":"thinking|derp","suggestions":[{"text":"str"}×6]}

Emotions: thinking(redirecting), derp(limitation). Default: thinking"""

        user_message = f"""Q: {question}

Context: {weak_context}

Can't fully answer. Acknowledge topic. Mention related info. Suggest 6 alternatives, each max 45 characters. Note: can discuss in interview. JSON only."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=700,
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

