import os
from typing import List
from openai import OpenAI

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-4o-mini"
    
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
    
    def generate_chat_response(self, prompt: str, context: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant answering questions about James Dawson's background, skills, and projects. Use the provided context to give accurate, personalized responses in first person as if you are James."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {prompt}"}
        ]
        
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def generate_redirect_response(self, question: str, weak_context: str) -> str:
        messages = [
            {
                "role": "system",
                "content": """You are a helpful assistant for James Dawson's portfolio chatbot. 
When you don't have enough information to fully answer a question, acknowledge 
this honestly but helpfully suggest 2-3 specific related questions that you 
CAN answer well based on the weak context provided."""
            },
            {
                "role": "user",
                "content": f"""Question: {question}

Available context (limited):
{weak_context}

I don't have enough detailed information to fully answer this question. 
Based on what limited context I do have, please:
1. Briefly acknowledge what the question is asking about
2. Mention what related information I DO have (based on context)
3. Suggest 2-3 specific alternative questions I can answer well

Keep the response friendly, honest, and helpful. Make it clear James can 
discuss this topic in detail during an actual interview."""
            }
        ]
        
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content
    
    def generate_off_topic_response(self) -> str:
        return """That seems outside the scope of my portfolio knowledge base. I'm here to answer questions about James's professional experience, technical skills, and project work.

What would you like to know about his development experience, projects, or technical approach?"""
    
    def generate_boundary_response(self) -> str:
        return """I'm here to help you learn about James's professional background and experience. Please keep questions professional and on-topic.

If you're interested in James's work, I'd be happy to answer questions about his technical skills, projects, or development approach."""

