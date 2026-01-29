# Atomic Notes Technical Specification

Technical deep-dive into how embeddings, vector search, and RAG work in the Folio system.

## Introduction

This document explains the technical foundation of the Folio RAG (Retrieval Augmented Generation) system. Understanding how embeddings and vector similarity search work will help you appreciate why the atomic notes structure matters and how to optimize notes for best performance.

For practical guidance on writing notes, see [ATOMIC-NOTES-GUIDE.md](ATOMIC-NOTES-GUIDE.md).

### System Overview

The Folio RAG system uses three key technologies:
- **OpenAI text-embedding-3-small**: Converts text to semantic vectors
- **Local JSON Storage**: Stores embeddings locally for fast retrieval
- **NumPy**: Performs cosine similarity calculations for semantic search
- **LangChain**: Orchestrates retrieval and generation

The system transforms your knowledge base (atomic notes) into embeddings, stores them locally, and retrieves relevant notes based on semantic similarity to user questions. The LLM then synthesizes these notes into coherent answers.

### Confidence Threshold Strategy

The system implements a smart confidence-based response strategy to handle questions with weak note coverage:

- **High Confidence (score ≥ 0.40)**: System generates a detailed, personalized answer using all retrieved context
- **Low Confidence (score < 0.40)**: System acknowledges the limitation and suggests related questions with better coverage

This approach prevents hallucination, manages user expectations, reduces costs, and strategically redirects users to well-covered topics.

## How Embeddings Work

### What Are Embeddings?

Embeddings are numerical vector representations of text that capture semantic meaning. They convert words, sentences, or documents into fixed-size arrays of numbers where similar meanings map to similar vectors.

**Conceptual Example:**
```
Text: "I have 3 years of React experience"
↓
Embedding Model (text-embedding-3-small)
↓
Vector: [0.023, -0.145, 0.892, ..., 0.341]  (1536 numbers)
```

Each number in the vector captures some aspect of meaning. The model learns these dimensions during training on large text datasets.

### Mathematical Representation

An embedding is a point in high-dimensional space:

```
Vector v ∈ ℝ^1536

Where each dimension captures semantic features:
v[0] might encode "programming-related" 
v[1] might encode "frontend technology"
v[2] might encode "experience level"
... and so on for 1536 dimensions
```

### Semantic Similarity

Similar texts produce similar vectors. We measure similarity using cosine similarity:

```python
def cosine_similarity(v1, v2):
    """
    Measures the angle between two vectors.
    Returns value between -1 and 1:
    - 1.0 = identical direction (very similar)
    - 0.0 = perpendicular (unrelated)
    - -1.0 = opposite direction (very different)
    """
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude1 = (sum(a * a for a in v1)) ** 0.5
    magnitude2 = (sum(b * b for b in v2)) ** 0.5
    return dot_product / (magnitude1 * magnitude2)
```

**Example:**
```
question_vec = [0.5, 0.3, 0.8, ...]  # "What technologies did you use?"
note_vec = [0.6, 0.2, 0.7, ...]      # "React Experience" note

similarity = cosine_similarity(question_vec, note_vec)
# Result: 0.89 (very similar!)
```

### Why Embeddings Work for Semantic Search

The embedding model (text-embedding-3-small) was trained on diverse text to capture:

1. **Semantic meaning**: "React" and "frontend framework" are related
2. **Context**: "Python" (language) vs "python" (snake) based on context
3. **Relationships**: "used in projects" relates to "technologies" and "experience"
4. **Synonyms**: "built" ≈ "created" ≈ "developed"
5. **Topics**: Groups related concepts (programming, web development, etc.)

This means:
```
Similar questions find similar notes:
- "What technologies did you use?" 
- "Tell me about your tech stack"
- "What programming languages do you know?"

All three would retrieve similar notes about technologies/skills,
even though the words are different.
```

### Embeddings vs Keyword Search

**Traditional Keyword Search:**
```
User asks: "What frameworks have you used?"
Keyword search might miss:
- "React" (doesn't contain "framework")
- "I used React" (different word order)
- "Frontend libraries" (different terminology)
```

**Embedding-Based Search:**
```
User asks: "What frameworks have you used?"
Embedding search finds:
- "React Experience" note (semantically similar)
- "Frontend libraries" note (related concept)
- "UI frameworks" note (synonymous)

Because all have similar embeddings to the question.
```

## The Embedding Model: text-embedding-3-small

### Specifications

- **Model**: OpenAI's `text-embedding-3-small`
- **Dimensions**: 1536 numbers per embedding
- **Training**: Trained on diverse text to capture semantic relationships
- **Cost**: ~$0.02 per 1M tokens (very affordable)
- **Performance**: Fast inference, suitable for real-time applications

### What It Captures

The model understands:
- **Semantic relationships**: "backend" ↔ "server-side" ↔ "API"
- **Technical concepts**: "React" ↔ "component" ↔ "JSX"
- **Actions**: "built" ↔ "created" ↔ "developed" ↔ "implemented"
- **Domains**: Programming, web development, databases, etc.
- **Context**: Same word different meanings based on context

### Example: Multi-word Concepts

```python
# These all produce similar embeddings:
embedding_1 = embed("React frontend framework")
embedding_2 = embed("UI library for building interfaces")
embedding_3 = embed("Component-based view layer")

# Cosine similarity between them: ~0.75-0.85 (high)
```

The model captures that these phrases describe similar concepts even though they use different words.

## RAG System Architecture

### Complete Flow Diagram

```
1. Knowledge Base Preparation (One-time)
   Atomic Notes → Embeddings → Stored in Pinecone
   
2. User Question (Per request)
   Question → Embedding → Vector Search → Retrieve Notes
   
3. Context Assembly
   Retrieved Notes + Compact Context → Prompt
   
4. LLM Generation
   Prompt → gpt-4o-mini → Answer
   
5. Response
   Answer + Suggestions + Source Documents
```

### Step 1: Knowledge Base Preparation

**One-time setup when notes are created or updated:**

```python
# Load atomic note
note_content = """
# React Frontend Development Experience

I have 3 years of professional experience with React, using it as my 
primary frontend framework for building interactive web applications...
"""

# Generate embedding
from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=note_content
)
embedding = response.data[0].embedding  # 1536 numbers

# Store in Pinecone
from pinecone import Pinecone
pc = Pinecone(api_key="...")
index = pc.Index("portfolio-notes")

index.upsert(
    vectors=[{
        "id": "react-experience-001",
        "values": embedding,  # 1536-dimensional vector
        "metadata": {
            "title": "React Experience",
            "type": "skill",
            "technology": "React",
            "content": note_content
        }
    }]
)
```

### Step 2: Question Embedding

**When user asks a question:**

```python
question = "What technologies did you use in your projects?"

# Embed the question
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)
question_embedding = response.data[0].embedding  # 1536 numbers
```

### Step 3: Vector Similarity Search

**Pinecone finds most similar vectors:**

```python
# Query Pinecone
results = index.query(
    vector=question_embedding,
    top_k=5,  # Retrieve top 5 most similar
    include_metadata=True
)

# Results ranked by similarity score (cosine similarity)
# Example results:
# [
#   {"id": "react-experience-001", "score": 0.89, "metadata": {...}},
#   {"id": "nexus-project-002", "score": 0.85, "metadata": {...}},
#   {"id": "python-backend-003", "score": 0.82, "metadata": {...}},
#   {"id": "fastapi-experience-004", "score": 0.80, "metadata": {...}},
#   {"id": "postgresql-db-005", "score": 0.78, "metadata": {...}}
# ]
```

**How Pinecone Works:**
- Stores vectors in an optimized index structure
- Uses approximate nearest neighbor (ANN) algorithms for fast search
- Can handle millions of vectors with sub-second query times
- Returns results sorted by similarity score

### Step 4: Context Assembly

**Build context from retrieved notes:**

```python
# Format retrieved notes
context_parts = []
for i, result in enumerate(results):
    note_content = result['metadata']['content']
    context_parts.append(f"=== Note {i+1}: {result['metadata']['title']} ===\n{note_content}")

retrieved_context = "\n\n".join(context_parts)

# Get compact conversation context
compact_context = get_compact_context(session_id)

# Build complete prompt
prompt = f"""You are Folio, an AI assistant representing James Dawson.
Use the following context to answer questions about his experience, skills, and projects.
Answer in first person as if you are James.

Retrieved Knowledge:
{retrieved_context}

Conversation Context:
{compact_context}

Question: {question}

Answer:"""
```

### Step 5: LLM Generation

**LLM synthesizes answer from context:**

```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are Folio, answering as James."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7
)

answer = response.choices[0].message.content
```

**What the LLM does:**
1. Reads all retrieved notes
2. Identifies relevant information for the question
3. Combines information from multiple notes
4. Filters out irrelevant details
5. Structures the answer naturally
6. Maintains first-person voice

### Step 6: Response

```python
return {
    "answer": answer,
    "suggestions": generate_suggestions(answer),
    "sources": [
        {"title": r['metadata']['title'], "score": r['score']} 
        for r in results
    ]
}
```

## Why Note Structure Matters

### Retrieval Optimization

**The embedding must capture the right information:**

Good note structure → Better embeddings → Better retrieval

**Example:**

```markdown
# Bad Note (won't retrieve well)
React. Used it. 3 years.
```
Problem: Too short, no context, embedding won't capture much

```markdown
# Good Note (retrieves well)
I have 3 years of professional experience with React, using it as my 
primary frontend framework for building interactive web applications.
I've used React in production applications including Nexus Job Manager 
and Folio, where I implemented complex user interfaces...
```
Success: Natural language, synonyms, context → rich embedding

### Synthesis Optimization

**The LLM needs clear, complete information:**

Well-written notes → Better synthesis → Better answers

**Example:**

If only this note is retrieved:
```markdown
# React
I know React.
```
LLM has almost nothing to work with.

If this note is retrieved:
```markdown
# React Frontend Development Experience

I have 3 years of professional experience with React, using it as my 
primary frontend framework for building interactive web applications.
I've used React in production applications including Nexus Job Manager,
where I built a complex job tracking interface with real-time updates, 
and Folio, my portfolio chatbot with smooth animations and dynamic UI 
components.

I'm experienced with React Hooks, Context API, React Query for data 
fetching, and React Router for navigation. I focus on component 
composition patterns, creating reusable component libraries, and 
optimizing React applications for performance.
```
LLM has rich information to synthesize a comprehensive answer.

### Token Efficiency

**Context window limits matter:**

- gpt-4o-mini has 128K token context limit
- Typical note: 200-500 tokens
- 5 retrieved notes: 1,000-2,500 tokens
- Compact context: ~500 tokens
- Prompt template: ~200 tokens
- **Total input: ~1,700-3,200 tokens** (well within limits)

If notes were 2,000 tokens each:
- 5 notes = 10,000 tokens
- Might need to retrieve fewer notes or truncate
- Less context = potentially worse answers

**Optimal size (200-500 tokens) balances:**
- Enough information to be useful
- Focused enough to stay on topic
- Small enough to fit multiple notes in context

### Context Quality

**Self-contained notes improve reliability:**

Problem: If notes reference each other:
```markdown
# React Project
As mentioned in my React experience note, I used it in this project...
```

If the "React experience note" isn't retrieved, this note makes no sense.

Solution: Self-contained notes:
```markdown
# Nexus Job Manager - React Frontend

I built the frontend for Nexus Job Manager using React as the primary 
framework. I have 3 years of React experience, and this project 
demonstrated my ability to build complex user interfaces...
```

Each note works alone, providing complete context.

## Vector Similarity Search Deep Dive

### How Pinecone Indexes Work

Pinecone uses specialized data structures for fast similarity search:

1. **Vector Indexing**: Stores vectors in an optimized structure
2. **Approximate Nearest Neighbor (ANN)**: Fast approximate search
3. **Sharding**: Distributes vectors across multiple machines for scale
4. **Metadata Storage**: Stores metadata alongside vectors

**Query Process:**
```
1. Receive query vector (1536 dimensions)
2. Search index for nearest neighbors
3. Calculate similarity scores (cosine similarity)
4. Sort by score
5. Return top-k results with metadata
```

**Performance:**
- Millions of vectors: <100ms query time
- Scales horizontally
- High availability

### Similarity Score Interpretation

```
Score > 0.85: Highly relevant (excellent match)
Score 0.75-0.85: Very relevant (good match)
Score 0.65-0.75: Relevant (okay match)
Score 0.40-0.65: Marginal relevance (weak match)
Score < 0.40: Low relevance (insufficient coverage)
```

**Confidence Threshold Implementation:**

The Folio system uses a confidence threshold of **0.40** to determine response strategy:

- **High Confidence (≥ 0.40)**: Generate detailed answer using full context
- **Low Confidence (< 0.40)**: Acknowledge limitation and redirect to better-covered topics

This approach balances coverage completeness with response quality, ensuring users receive helpful guidance even when specific questions aren't well-covered.

## LLM Synthesis Process

### How the LLM Combines Multiple Notes

The LLM receives:
```
Retrieved Note 1: React experience (3 years, projects, skills)
Retrieved Note 2: Nexus Job Manager project (React + Python)
Retrieved Note 3: Python backend experience (FastAPI, databases)
```

And synthesizes:
```
Answer: I've used a variety of technologies across my projects. For 
frontend development, I primarily use React with TypeScript, which I've 
been working with for 3 years. I used React in projects like Nexus Job 
Manager, where I built a microfrontend architecture, and in my Folio 
portfolio chatbot.

For backend development, I use Python with FastAPI to build REST APIs 
and web services. In Nexus Job Manager, I connected the FastAPI backend 
to a PostgreSQL database, designed the schema, and handled authentication.

So my main tech stack includes React and TypeScript for frontend, Python 
and FastAPI for backend, and PostgreSQL for databases.
```

**What the LLM did:**
1. Identified relevant information from each note
2. Combined information coherently
3. Structured the answer logically
4. Maintained first-person voice
5. Filtered out irrelevant details

### Chain-of-Thought Processing

While not explicit, the LLM effectively:
1. Analyzes the question
2. Scans retrieved notes for relevant info
3. Identifies key points to address
4. Organizes information logically
5. Generates natural language response

This is why well-written notes matter: the LLM can extract and combine information more effectively when notes are clear, complete, and naturally written.

## Confidence Threshold Strategy

### Overview

The confidence threshold strategy addresses a key challenge in RAG systems: what to do when retrieved notes have low relevance to the question. Rather than attempting to answer every question (risking hallucination or unhelpful responses), the system uses similarity scores to determine the best response strategy.

### The Problem

Testing with 200 diverse interview questions revealed that approximately 20% of questions had weak note coverage (top similarity score < 0.40). Attempting to answer these questions with low-relevance notes produces:

1. **Hallucination**: LLM fills gaps with invented information
2. **Vague responses**: Generic answers that don't help the user
3. **Wasted tokens**: Full LLM generation for poor-quality output
4. **Bad UX**: User receives unhelpful answer with no guidance

### The Solution

The system implements a dual-mode response strategy based on the top similarity score:

```python
CONFIDENCE_THRESHOLD = 0.40

if top_similarity_score >= CONFIDENCE_THRESHOLD:
    # HIGH CONFIDENCE MODE
    # Generate detailed, personalized answer
    # Use full context from retrieved notes
    # Max tokens: 500
    # Temperature: 0.7
else:
    # LOW CONFIDENCE MODE
    # Acknowledge limitation honestly
    # Suggest related questions with better coverage
    # Max tokens: 200 (cheaper)
    # Temperature: 0.7
```

### High Confidence Response (≥ 0.40)

**Prompt Structure:**

```python
system_message = """You are a helpful assistant answering questions about 
James Dawson's background, skills, and projects. Use the provided context 
to give accurate, personalized responses in first person as if you are James."""

user_message = f"""Context:\n{context}\n\nQuestion: {question}

Answer this question in detail using the context provided."""
```

**Example:**

```
Q: "Tell me about your Python experience"
Top Score: 0.82 (High Confidence)

Retrieved Notes:
1. python-backend-experience (0.82)
2. whatnow-deployment-and-links (0.75)
3. folio-rag-system-architecture (0.71)

Response: "I have extensive Python experience, primarily focused on 
backend development with FastAPI and Flask. I've built several production 
applications including WhatNow, a contextual bandits recommendation system, 
and Folio, this AI portfolio chatbot. In these projects, I've worked with 
FastAPI for REST APIs, SQLAlchemy for database interactions, and integrated 
with services like OpenAI and Railway for deployment..."
```

### Low Confidence Response (< 0.40)

**Prompt Structure:**

```python
system_message = """You are a helpful assistant for James Dawson's portfolio chatbot. 
When you don't have enough information to fully answer a question, acknowledge 
this honestly but helpfully suggest 2-3 specific related questions that you 
CAN answer well based on the weak context provided."""

user_message = f"""Question: {question}

Available context (limited):
{context}

I don't have enough detailed information to fully answer this question. 
Based on what limited context I do have, please:
1. Briefly acknowledge what the question is asking about
2. Mention what related information I DO have (based on context)
3. Suggest 2-3 specific alternative questions I can answer well

Keep the response friendly, honest, and helpful. Make it clear James can 
discuss this topic in detail during an actual interview."""
```

**Example:**

```
Q: "What's your typical workday like?"
Top Score: 0.31 (Low Confidence)

Retrieved Notes:
1. my-work-style-and-preferences (0.31)
2. handling-stress-and-pressure (0.28)
3. work-life-balance-approach (0.26)

Response: "I don't have specific details about James's typical workday 
routine stored in my knowledge base. However, I can share information 
about his work style, how he manages priorities, and his approach to 
work-life balance.

You might want to ask:
• How does James approach work-life balance?
• What's James's work style and preferences?
• How does James handle stress and tight deadlines?

These are topics I have more detailed information about. For specifics 
about daily routines, James would be happy to discuss this in an interview!"
```

### Benefits

1. **Prevents Hallucination**: System doesn't attempt to answer with insufficient context
2. **Better UX**: Users get honest, helpful redirection instead of vague answers
3. **Cost Savings**: Low-confidence responses use ~60% fewer tokens (200 vs 500 max)
4. **Strategic Redirection**: Guides users toward well-covered strengths
5. **Transparent Limitations**: Builds trust by being honest about knowledge gaps
6. **Interview Opportunity**: Frames limitations as conversation starters for real interviews

### Implementation Details

**Response Flow:**

```python
def generate_response(question: str, session_id: str):
    # 1. Embed question
    query_embedding = openai_service.get_embedding(question)
    
    # 2. Retrieve similar notes
    similar_notes = embedding_storage.find_similar_notes(
        query_embedding, 
        k=5
    )
    
    # 3. Check confidence
    top_score = similar_notes[0]['score'] if similar_notes else 0
    
    # 4. Build context
    context = build_context_from_notes(similar_notes)
    
    # 5. Route based on confidence
    if top_score >= CONFIDENCE_THRESHOLD:
        # HIGH CONFIDENCE: Full answer
        response = openai_service.generate_chat_response(
            question=question,
            context=context,
            mode="full_answer",
            max_tokens=500,
            temperature=0.7
        )
        
        return {
            "answer": response,
            "confidence": "high",
            "top_score": top_score,
            "mode": "direct_answer"
        }
    else:
        # LOW CONFIDENCE: Redirect
        response = openai_service.generate_redirect_response(
            question=question,
            weak_context=context,
            max_tokens=200,
            temperature=0.7
        )
        
        return {
            "answer": response,
            "confidence": "low",
            "top_score": top_score,
            "mode": "redirect"
        }
```

### Threshold Tuning

The 0.40 threshold was determined through empirical testing:

**Testing Process:**
1. Ran 200 diverse interview questions through the system
2. Manually evaluated response quality at different score ranges
3. Identified score ranges where responses degraded significantly
4. Set threshold at the boundary between "adequate" and "weak" responses

**Score Range Analysis:**
- **0.70+**: Excellent responses (19% of questions)
- **0.50-0.69**: Good responses (33% of questions)
- **0.40-0.49**: Adequate responses (27% of questions)
- **0.30-0.39**: Weak responses (15% of questions)
- **<0.30**: Very weak responses (6% of questions)

Setting the threshold at **0.40** captures the boundary where response quality significantly drops, ensuring:
- ~79% of questions receive full answers (high coverage)
- ~21% receive helpful redirects (quality control)
- Optimal balance between coverage and quality

### Cost Impact

**Scenario: 100 questions**

Without confidence threshold:
- 100 questions × 500 tokens avg = 50,000 tokens
- Cost: ~$0.01

With confidence threshold (assuming 21% low-confidence):
- 79 high-confidence × 500 tokens = 39,500 tokens
- 21 low-confidence × 200 tokens = 4,200 tokens
- Total: 43,700 tokens
- Cost: ~$0.0087
- **Savings: 13%** + improved response quality

### Future Enhancements

Potential improvements to the confidence threshold system:

1. **Dynamic Thresholding**: Adjust threshold based on question category
2. **Graduated Responses**: Multiple confidence tiers (e.g., 0.60, 0.40, 0.20)
3. **Feedback Loop**: Learn from user reactions to adjust threshold
4. **Context-Aware Routing**: Consider conversation history when routing
5. **Fallback Sources**: Attempt web search for low-confidence questions

## Performance Considerations

### Token Limits

**Context window:**
- Input: 128K tokens (gpt-4o-mini)
- Typical usage: 2-3K tokens input
- Plenty of headroom for future growth

**Cost optimization:**
- Smaller notes = more notes in context window
- But too small = not enough information
- 200-500 tokens per note is the sweet spot

### Retrieval Quality

**Factors affecting retrieval:**
1. **Note quality**: Well-written notes embed better
2. **Note size**: 200-500 tokens optimal
3. **Top-k value**: 3-5 notes usually sufficient
4. **Embedding model**: text-embedding-3-small is excellent
5. **Note coverage**: Multiple notes on important topics

**Improving retrieval:**
- Write focused, self-contained notes
- Use natural language with synonyms
- Cover topics from multiple angles
- Include question-like phrases

### Synthesis Quality

**Factors affecting synthesis:**
1. **Retrieved notes quality**: Clear, complete information
2. **Number of notes**: 3-5 usually optimal
3. **Note coherence**: Related information connects better
4. **Prompt design**: Clear instructions to LLM
5. **Temperature**: 0.7 balances creativity and accuracy

**Improving synthesis:**
- Write notes that work alone and together
- Include complete context in each note
- Use consistent terminology across notes
- Structure information logically within notes

### Query Performance

**Typical latencies:**
- Embedding generation: 50-100ms
- Pinecone query: 50-100ms
- LLM generation: 1-3 seconds
- **Total response time: 1.2-3.2 seconds**

This is acceptable for a conversational interface.

## Technical Implementation with LangChain

### LangChain RAG Chain

LangChain orchestrates the RAG process:

```python
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class RAGService:
    def __init__(self):
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )
        
        # Connect to Pinecone vector store
        self.vectorstore = Pinecone.from_existing_index(
            index_name="portfolio-notes",
            embedding=self.embeddings
        )
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7
        )
        
        # Create prompt template
        self.prompt = PromptTemplate(
            template="""You are Folio, an AI assistant representing James Dawson.
            Use the following context to answer questions about his experience, skills, and projects.
            
            Context: {context}
            
            Question: {question}
            
            Answer in first person as if you are James:""",
            input_variables=["context", "question"]
        )
        
        # Create retrieval chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # Concatenate all docs
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}  # Top 5 results
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
    
    async def get_response(self, question: str):
        # LangChain handles:
        # 1. Embedding the question
        # 2. Querying Pinecone
        # 3. Formatting context
        # 4. Building prompt
        # 5. Calling LLM
        # 6. Returning result with sources
        
        result = self.qa_chain({"query": question})
        
        return {
            "answer": result["result"],
            "sources": result["source_documents"]
        }
```

### Chain Types

LangChain supports different chain types:

1. **"stuff"** (recommended): Concatenate all documents
   - Simple, works well for 3-5 documents
   - Used when total tokens < context limit

2. **"map_reduce"**: Process each document separately, then combine
   - For very long documents or many documents
   - More expensive (multiple LLM calls)

3. **"refine"**: Iteratively refine answer with each document
   - For when order matters
   - Most expensive (sequential LLM calls)

For Folio with 3-5 notes of 200-500 tokens each, "stuff" is optimal.

## Summary

### Key Technical Concepts

1. **Embeddings**: Transform text to semantic vectors (1536 dimensions)
2. **Cosine Similarity**: Measure angle between vectors to find similar content
3. **Vector Search**: Fast approximate nearest neighbor search in Pinecone
4. **RAG**: Retrieve relevant notes, generate answer with LLM
5. **Synthesis**: LLM combines multiple notes into coherent answer

### Why It Works

- Embeddings capture semantic meaning, not just keywords
- Similar meanings produce similar vectors
- Vector search finds relevant information quickly
- LLM synthesizes information into natural language
- Well-written notes optimize every step of the process

### Best Practices

1. Write notes in natural language (200-500 tokens)
2. Make notes self-contained and focused
3. Include synonyms and related terms
4. Cover topics from multiple angles
5. Use consistent terminology across notes

For practical guidance on writing notes, see [ATOMIC-NOTES-GUIDE.md](ATOMIC-NOTES-GUIDE.md).

