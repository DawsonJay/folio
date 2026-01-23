# Folio - Design Notes

## Project Overview

**Project Name**: Folio  
**AI Assistant Name**: Folio  
**GitHub Repository**: https://github.com/DawsonJay/folio

Folio is a minimalist portfolio website featuring an AI chatbot assistant that answers questions about skills, experience, and projects using RAG (Retrieval Augmented Generation). The name "Folio" references both portfolio and evokes growth (foliage), representing a living, evolving portfolio.

## Core Concept

A minimalist portfolio website with 2 pages:
1. **Landing page** - AI chatbot interface with single AI message bubble (primary interaction)
   - Shows one AI response bubble that updates with each answer
   - Clean, focused interface - no scrolling chat history
   - More approachable, less intimidating than full chat interface
   - Download button for conversation export (if needed)
2. **Contact page** - Traditional contact form

### Key Value Propositions
- **Efficiency for employers** - Find specific skills/technologies instantly without browsing
- **Comprehensive access** - All data available, nothing hidden due to space constraints
- **Demonstrates LLM skills** - Directly shows capability with AI/LLM technologies
- **Elegant simplicity** - Focus all effort on one exceptional experience
- **Data-driven improvement** - Track questions and metrics to optimize over time

## Technical Architecture

### LLM & API
- **Provider**: OpenAI (existing account)
- **Embeddings**: `text-embedding-3-small` ($0.02 per 1M tokens)
- **Chat Model**: `gpt-4o-mini` ($0.15/$0.60 per 1M tokens input/output)
- **Persona**: First person ("I know JS" not "James knows JS")  
**AI Assistant Name**: Folio

### RAG (Retrieval Augmented Generation) System
- **Framework**: LangChain (industry-standard RAG orchestration)
- **Vector Database**: Pinecone (free tier: 1 index, 100k vectors, 5M queries/month)
- **Embedding Model**: `text-embedding-3-small` (1536 dimensions)
- **RAG Chain**: LangChain RetrievalQA or RetrievalQAWithSourcesChain

### RAG Flow (via LangChain)
1. User asks question → LangChain handles the flow
2. LangChain converts question to embedding (OpenAIEmbeddings)
3. LangChain queries Pinecone vector store for similar notes
4. Retrieves top 3-5 relevant chunks (configurable via retriever)
5. LangChain builds prompt with retrieved context + compact conversation context
6. LLM generates answer using context
7. Returns answer + source documents
8. Compact context file updated with new information from exchange

### Conversation Context Management
- **Approach**: Compact context file (similar to Cursor IDE)
- **Strategy**: Build evolving context summary, not full conversation history
- **Benefits**: Context-aware responses without token bloat, scales to long conversations
- **Implementation**: 
  - Maintain compact context file per session
  - Update context after each exchange with key information
  - Include compact context in each prompt alongside RAG-retrieved notes
   - Store full conversation history for potential export/download functionality
- **Context Structure**: Captures topics discussed, skills/projects mentioned, user interests, key details
- **Update Strategy**: LLM-based or hybrid (entity extraction + LLM summarization)

## Data Structure

### Atomic Notes Approach
- **Format**: Markdown files, ~200-500 tokens each
- **Structure**: Self-contained, semantically coherent chunks
- **Overlap encouraged**: Multiple notes can reference same topics from different angles

### Note Types
- **Skill notes**: Technology/skill + experience level + professional use + projects
- **Project notes**: Tech stack + what was built + challenges + outcomes
- **Experience notes**: Role + technologies + achievements

### Example Note Structure
```markdown
# React Experience

**Skill Level:** Advanced (3 years professional experience)
**Professional Use:** Yes, used in 2 production applications
**Projects:**
- Nexus Job Manager (2024): Primary frontend framework, built microfrontend architecture
- Folio (2025): Interactive UI with real-time streaming, RAG-powered portfolio chatbot

**Technical Skills:**
- React Hooks, Context API, React Query, React Router
- Component composition patterns
- Performance optimization

**Preferred Patterns:**
[Details about approach and preferences]
```

### Key Principles
- **Semantic coherence**: Each note about one topic/concept
- **Self-contained**: Makes sense when retrieved alone
- **Optimal size**: 200-500 tokens per chunk
- **Overlapping allowed**: Skill notes + project notes can both mention React

## Rate Limiting Strategy

### Multi-tier API-style limits
- **5 questions per minute** (burst protection)
- **50 questions per hour** (sustained protection)
- **100 questions per day** (daily protection)

### Implementation
- Check all three limits on each request
- Store timestamps per IP address
- Use Redis or in-memory Map for fast lookups
- Clean up old entries periodically

### Rate Limit Messages
Include conversion opportunity:
```
"Rate limit reached (5 questions per minute). 
If you'd like to learn more, feel free to contact me for an interview!"
```

## Features & Enhancements

### Core Features
- **Header strip**: Dark strip at top with name and "Get in Touch" link
- AI chatbot with RAG-powered responses
- Single AI message bubble interface (updates with each response, no chat history)
- Animated AI avatar with facial expressions showing state (thinking, surprised, ready, etc.)
- Suggested questions on landing page
- Download conversation button (if needed)
- Contact page

### Recommended Enhancements
1. **AI Avatar with State Expressions** (HIGH PRIORITY)
   - Animated head/face showing different expressions based on AI state
   - **Design**: Single message bubble approach
     - Avatar appears with the single AI message bubble
     - Avatar animates to show current state (thinking, surprised, ready, etc.)
     - Always visible since there's only one message bubble
     - Clean, focused visual feedback
   - **Expressions** (6 total):
     1. **Happy**: Default/ready state - smiling face, welcoming
     2. **Thinking**: Processing questions - confused/questioning expression with floating question marks accent
     3. **Surprised**: Initial response moment - wide eyes, excited
     4. **Derp/Oops**: Dual purpose - AI errors OR unclear questions
     5. **Tired**: Rate limiting - sleepy expression with floating Z's accent
     6. **Annoyed**: Offensive questions - irritated expression with huff lines accent
   - **Component Structure**:
     - **Base Face Component**: Renders facial expression (eyes, mouth, etc.)
     - **Accent Component**: Separate overlay for animated accents (question marks, Z's, sparkles, huff lines)
     - Accents animate independently from the face for enhanced expressiveness
     - Benefits: Modular design, independent animations, performance optimization
   - **Expression Usage Flow**:
     1. Initial state: **Happy** (welcoming, ready for questions)
     2. Question asked: **Thinking** (with question marks)
     3. Response received: **Surprised** → **Happy** (brief excitement, then ready)
     4. Error scenarios: **Derp** (AI error or unclear question), **Tired** (rate limit), **Annoyed** (offensive)
   - Makes the AI feel more alive and responsive
   - Visual feedback enhances user experience

2. **Follow-up question suggestions** (HIGH PRIORITY)
   - After each answer, suggest 2-3 relevant follow-up questions
   - Generated by LLM or rule-based
   - Display as clickable buttons/chips
   - **Placement**: 
     - **Empty state**: Show prominent suggestions when no question has been asked
     - **After response**: Show follow-up suggestions below the AI response bubble
     - Keeps suggestions contextual and accessible
   - Encourages deeper exploration

3. **Project deep-dive links**
   - When project mentioned, offer: "See code" | "View demo" | "Learn more"
   - Makes answers actionable

4. **Conversation export** (on landing page)
   - Download button for chat history
   - Formats: PDF, JSON, Markdown, TXT
   - Useful for recruiters to share
   - Integrated into main chatbot interface

5. **Analytics dashboard** (backend)
   - Track all questions asked
   - Most common questions
   - Technologies/skills inquired about
   - Projects mentioned
   - Question patterns
   - Drop-off points
   - Response times

### Analytics to Log
- Full question text
- Timestamp
- Response generated (or key points)
- Session ID
- Response time
- IP address (for rate limiting)

## Cost Estimates

### Monthly Costs (Low-Medium Traffic)
- **OpenAI API**: ~$0.05-1.00/month
  - Embeddings: ~$0.001 one-time setup
  - Chat: ~$0.0001 per conversation
- **Vector Database**: $0 (Pinecone free tier)
- **Backend Hosting**: Already covered (Railway account)
- **Frontend Hosting**: $0 (Vercel/Netlify free tiers)
- **Database**: Included with Railway account
- **Redis**: Included with Railway or Upstash free tier
- **Total**: ~$0-1/month for typical portfolio traffic (mostly just OpenAI)

### Cost Optimization
- Cache common questions
- Rate limiting prevents abuse
- Use `gpt-4o-mini` (cost-effective)
- Monitor usage with alerts

## Implementation Phases

### Phase 1: MVP
1. Simple chatbot interface
2. Basic RAG with vector database
3. Atomic notes knowledge base
4. Rate limiting
5. Contact page

### Phase 2: Enhancements
1. Follow-up question suggestions
2. Analytics logging
3. Project deep-dive links
4. Conversation export
5. Compact context file implementation

### Phase 3: Optimization
1. Analytics dashboard
2. A/B testing
3. Performance optimization
4. Content refinement based on data

## Key Decisions Made

### Design Decisions
- **Project & AI Name: Folio** - Portfolio reference + growth/foliage metaphor, memorable name for the AI assistant
- **Color Theme: Dark forest green with warm accents** - Dark green background with soft off-white UI elements, warm terracotta accents, and muted teal-green secondary elements. Evokes growth and nature, connects to "foliage" concept, professional and approachable
- **First person voice** ("I" not "James") - more engaging
- **Atomic notes structure** - precise retrieval, easy updates
- **Overlapping notes** - different angles, better coverage
- **Multi-tier rate limiting** - prevents abuse, allows exploration
- **Rate limit → contact conversion** - turns limitation into opportunity
- **Follow-up suggestions** - encourages deeper engagement
- **Compact context file** - Cursor-style approach: build evolving context summary instead of full conversation history
  - Context-aware responses without token bloat
  - Scales to long conversations
  - Lower cost than full history
  - Full conversation stored separately for display on landing page

### Technical Decisions
- **Python-heavy backend** - Impressive project, demonstrates Python skills
- **FastAPI** - Modern, async, production-ready
- **LangChain** - Popular in job listings, industry-standard RAG framework
- **SQLAlchemy** - Seen in job listings, shows ORM expertise
- **Railway deployment** - Already have account, simple deployment
- **PostgreSQL on Railway** - Integrated database service
- **OpenAI + Pinecone** - Existing account, free tier available
- **Separate frontend/backend** - Full-stack architecture demonstration

## Technical Stack (Final Decisions)

### Backend (Python-heavy)
- **Framework**: FastAPI (modern, async, auto-docs)
- **RAG Framework**: LangChain (industry-standard, popular in job listings)
- **LLM Integration**: OpenAI SDK (via LangChain)
- **Vector DB**: Pinecone (via LangChain)
- **Database ORM**: SQLAlchemy (industry-standard, seen in job listings)
- **Database**: PostgreSQL (Railway database service)
- **Migrations**: Alembic (SQLAlchemy migrations)
- **Rate Limiting**: Redis (Railway Redis service or Upstash)
- **Data Validation**: Pydantic (comes with FastAPI)
- **Deployment**: Railway (already have account)

### Frontend
- **Framework**: React + TypeScript
- **Build Tool**: Vite (fast dev experience)
- **Styling**: Tailwind CSS
- **Architecture**: Event-driven, modular component system
- **Deployment**: Vercel/Netlify (free tiers)

### UI/Design Theme
- **Style**: Minimalist, single message bubble interface (clean and approachable)
- **Responsive Design**: 
  - **Mobile-first approach**: Design optimized for mobile screens
  - **Desktop**: Same design as mobile, background extends full width
  - **Content container**: Centered, max-width ~600px (consistent across all screen sizes)
  - **All elements**: Same size and spacing on mobile and desktop (avatar, speech bubble, input, suggestions)
  - **Background**: Full width on all screen sizes, content stays centered
- **Typography**: 
  - **Primary Font**: Plus Jakarta Sans - Friendly, modern, approachable, excellent readability
  - **Code Font**: JetBrains Mono - For code snippets and technical content
  - **Font Loading**: Google Fonts or @fontsource packages
- **AI Avatar**: Animated head/face with expressions showing AI state
  - Visual feedback for thinking, processing, ready states
  - Makes the AI feel more alive and responsive
  - Simple, cartoon-style expressions (happy, thinking, surprised, derp, tired, annoyed)
  - Separate accent components for independent animation (question marks, Z's, sparkles, huff lines)

### Color Palette
```css
/* Backgrounds */
--bg-primary: #1E2A26;        /* Main background */
--bg-header: #2D4A42;         /* Header strip */

/* UI Base Colors */
--ui-base: #F0F2F1;           /* Base light color - avatar skin, speech bubble, input field */
--accent: #D4A574;            /* Accent color - avatar hair, buttons, interactive icons */
--ui-secondary: #5B8A7A;      /* Secondary UI - suggested questions */

/* Primary Text Colors */
--primary-black: #1E2A26;     /* Primary dark - text on light backgrounds, facial features */
--primary-white: #E8E8D8;     /* Primary light - text on dark backgrounds, suggestions text */
```

**Color Usage:**
- **Backgrounds**: Dark forest green for main background and header
- **UI Base**: Soft off-white for avatar, speech bubble, and input field
- **Accent**: Warm terracotta for avatar hair and interactive elements
- **Secondary UI**: Muted teal-green for suggested questions
- **Text**: Dark green for text on light backgrounds and facial features; light beige for text on dark backgrounds

### Typography Scale
```css
/* Primary Font - Plus Jakarta Sans */
--font-heading: 'Plus Jakarta Sans', sans-serif;
--font-body: 'Plus Jakarta Sans', sans-serif;
--font-size-h1: 2rem;    /* 32px */
--font-size-h2: 1.5rem;  /* 24px */
--font-size-h3: 1.25rem; /* 20px */
--font-size-base: 1rem;   /* 16px */
--font-size-small: 0.875rem; /* 14px */

/* Code Font - JetBrains Mono */
--font-code: 'JetBrains Mono', monospace;
--font-size-code: 0.875rem; /* 14px */

/* Line heights */
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;
```

**Font Loading Options:**
- Google Fonts: https://fonts.google.com/specimen/Plus+Jakarta+Sans and https://fonts.google.com/specimen/JetBrains+Mono
- npm packages: `@fontsource/plus-jakarta-sans` and `@fontsource/jetbrains-mono`

### Responsive Design Implementation
```css
/* Container - centered, consistent max-width */
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Background extends full width naturally */
body {
  background-color: var(--bg-primary);
  min-height: 100vh;
}

/* Desktop - same design, just wider background */
@media (min-width: 768px) {
  .container {
    max-width: 600px;  /* Keep same max width */
    /* All elements maintain same size and spacing */
  }
}
```

**Key Principles:**
- Mobile-first design approach
- Content container stays centered with consistent max-width
- Background color extends to fill viewport width
- No element stretching or size changes between mobile and desktop
- Maintains focused, minimalist aesthetic across all screen sizes

### Key Python Libraries
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `langchain` - RAG orchestration
- `langchain-openai` - OpenAI integration
- `langchain-pinecone` - Pinecone integration
- `langchain-community` - Additional tools
- `sqlalchemy` - ORM
- `alembic` - Database migrations
- `psycopg2-binary` - PostgreSQL driver
- `redis` - Rate limiting/caching
- `pydantic` - Data validation
- `python-dotenv` - Environment variables

### Why This Stack
- **Python-heavy backend** - Demonstrates strong Python skills
- **LangChain** - Popular in job listings, industry-standard
- **SQLAlchemy** - Seen in multiple job listings, shows ORM skills
- **Railway** - Already paying for account, simple deployment
- **Full-stack architecture** - Shows backend + frontend skills
- **Production-ready** - Industry-standard tools throughout

### What Uses Python
**100% of backend is Python:**
- FastAPI application (Python)
- LangChain RAG orchestration (Python)
- OpenAI SDK integration (Python)
- Pinecone SDK integration (Python)
- SQLAlchemy database operations (Python)
- Rate limiting logic (Python)
- Analytics/logging (Python)
- Business logic (Python)
- Data processing (Python)

**Frontend is separate:**
- React + TypeScript (JavaScript)
- Makes HTTP requests to Python backend

## Project Architecture

### Backend Structure (Python)
```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   ├── chat.py          # Chat endpoint
│   │   ├── embeddings.py    # Embedding generation (if needed)
│   │   └── analytics.py     # Analytics endpoints
│   ├── services/
│   │   ├── rag_service.py   # LangChain RAG service
│   │   ├── openai_service.py # OpenAI wrapper
│   │   ├── pinecone_service.py # Pinecone wrapper
│   │   ├── context_manager.py # Compact context file management
│   │   └── rate_limiter.py  # Rate limiting logic
│   ├── models/              # SQLAlchemy models
│   │   ├── chat_message.py
│   │   ├── chat_session.py
│   │   └── analytics_event.py
│   ├── database.py          # Database connection (SQLAlchemy)
│   ├── schemas/             # Pydantic models
│   └── utils/
├── data/
│   └── notes/               # Atomic notes (markdown files)
├── alembic/                 # Database migrations
├── requirements.txt
├── .env.example
└── Dockerfile
```

### Frontend Structure (React/TypeScript)
```
frontend/
├── src/
│   ├── components/
│   │   ├── Chatbot.tsx      # Main chatbot component with single message bubble
│   │   ├── MessageBubble.tsx  # Single AI message bubble component
│   │   ├── FolioAvatar.tsx  # Animated AI avatar with emotion transitions
│   │   ├── InputBox.tsx
│   │   ├── FollowUpSuggestions.tsx
│   │   └── DownloadButton.tsx  # Chat history download
│   ├── events/
│   │   ├── eventBus.ts      # Central event system for component communication
│   │   └── eventTypes.ts    # Event type definitions
│   ├── hooks/
│   │   └── useEventBus.ts   # React hook for event system
│   ├── pages/
│   │   ├── LandingPage.tsx  # Chatbot page with single message bubble interface
│   │   ├── Header.tsx       # Top header strip with name and "Get in Touch" link
│   │   └── ContactPage.tsx
│   ├── api/
│   │   └── chatApi.ts       # API client
│   ├── types/
│   └── utils/
├── package.json
└── vite.config.ts
```

### LangChain Integration Example
```python
# services/rag_service.py
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = Pinecone.from_existing_index(
            index_name="portfolio-notes",
            embedding=self.embeddings
        )
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # Custom prompt template
        self.prompt = PromptTemplate(
            template="""You are Folio, an AI assistant representing James Dawson. 
            Use the following context to answer questions about his experience, skills, and projects.
            
            Context: {context}
            
            Question: {question}
            
            Answer in first person as if you are James:""",
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
    
    async def get_response(self, question: str):
        result = self.qa_chain({"query": question})
        return {
            "answer": result["result"],
            "sources": result["source_documents"]
        }
```

### SQLAlchemy Models Example
```python
# models/chat_message.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey("chat_sessions.id"))
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    response_time_ms = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("ChatSession", back_populates="messages")
```

## Next Steps

1. Set up project structure (backend + frontend)
2. Initialize FastAPI app with LangChain
3. Set up PostgreSQL on Railway
4. Create SQLAlchemy models and migrations
5. Create atomic notes knowledge base
6. Implement LangChain RAG system with Pinecone
7. Build chatbot UI (React + TypeScript)
8. Add rate limiting with Redis
9. Implement follow-up suggestions
10. Add analytics logging
11. Deploy backend to Railway
12. Deploy frontend to Vercel/Netlify
13. Test end-to-end

## Questions to Consider

- What format for atomic notes? (Markdown files, JSON, database?)
- How to structure note metadata? (tags, types, relationships?)
- Should notes be version controlled?
- How to handle note updates? (re-embedding strategy)
- What analytics visualization needed?
- Should there be an admin interface for managing notes?

## Conversation Context Implementation Details

### Compact Context File Structure
```python
# Example structure
compact_context = {
    "topics_discussed": ["React", "Python", "FastAPI"],
    "projects_mentioned": ["Nexus Job Manager", "Folio"],
    "user_interests": ["backend architecture", "RAG systems"],
    "key_details": {
        "React": "3 years experience, used in production",
        "Python": "preferred for backend, FastAPI experience"
    },
    "conversation_focus": "Full-stack development with Python backend"
}
```

### Implementation Options
1. **LLM-Based Context Building**: Use LLM to update context after each exchange
2. **Hybrid Approach**: Extract entities automatically + LLM summarization
3. **LangChain ConversationSummaryMemory**: Use built-in with custom summarization prompt

### Context Management Considerations
- **Update frequency**: After each message vs. periodic updates
- **Context size limits**: Max tokens, pruning strategy
- **Reset strategy**: Per session, time-based, or topic shift detection
- **Storage**: In-memory per session, or persisted in database/Redis

## Frontend Architecture

### Event-Driven Component System
- **Architecture**: Modular components communicate via centralized event system
- **Benefits**: 
  - Decoupled components (easy to test and maintain)
  - Components can request actions from other components
  - Clean separation of concerns
  - Easy to add new components without tight coupling

### Event System Implementation
```typescript
// events/eventTypes.ts
export type AvatarEmotion = 
  | 'happy' 
  | 'thinking' 
  | 'surprised' 
  | 'derp' 
  | 'tired' 
  | 'annoyed';

export type AccentType = 
  | 'questionMarks'  // For thinking
  | 'sparkles'       // For surprised
  | 'zzz'            // For tired
  | 'huff'           // For annoyed
  | null;            // No accent (happy, derp)

export type ChatEvent = 
  | { type: 'avatar:setEmotion', emotion: AvatarEmotion }
  | { type: 'chat:questionAsked' }
  | { type: 'chat:responseReceived' }
  | { type: 'chat:error' };

// events/eventBus.ts
class EventBus {
  private listeners: Map<string, Function[]> = new Map();
  
  on(event: string, callback: Function) {
    // Register listener
  }
  
  emit(event: string, data?: any) {
    // Emit event to all listeners
  }
  
  off(event: string, callback: Function) {
    // Remove listener
  }
}

// hooks/useEventBus.ts
export function useEventBus() {
  // React hook wrapper for event bus
}
```

### Avatar Component Architecture
```typescript
// components/FolioAvatar.tsx
interface FolioAvatarProps {
  // Minimal props, listens to events
}

// Separate components for modularity
<AvatarContainer>
  <AvatarFace expression={currentExpression} />
  {accent && <AvatarAccent type={accent} />}
</AvatarContainer>

// Accent types and their animations
type AccentType = 'questionMarks' | 'zzz' | 'sparkles' | 'huff' | null;

// Animation possibilities:
// - Question marks: subtle float/rotation while thinking
// - Z's: gentle drift upward when tired
// - Sparkles: twinkle/pulse on surprise
// - Huff lines: brief puff animation when annoyed
// - Face: minimal or no animation (stays stable)

// Other components emit events to request emotions:
// eventBus.emit('avatar:setEmotion', 'thinking')
// eventBus.emit('avatar:setEmotion', 'happy')
```

### Avatar Image Assets
**Location**: `frontend/src/assets/avatar/`

**Base Face Expressions** (6 total):
- `face-happy.png` - Default/ready state
- `face-thinking.png` - Processing questions
- `face-surprised.png` - Initial response moment
- `face-derp.png` - AI errors or unclear questions
- `face-tired.png` - Rate limiting
- `face-annoyed.png` - Offensive questions

**Accent Components** (4 total):
- `accent-question-marks.png` - For thinking expression
- `accent-sparkles.png` - For surprised expression
- `accent-zzz.png` - For tired expression
- `accent-huff.png` - For annoyed expression

**Export Settings** (for web use):
- Format: PNG
- Compression: 6-9 (optimized for web)
- Force convert to sRGB: ✓
- Store alpha channel (transparency): ✓
- Force convert to 8 bits/channel: ✓

### Component Communication Flow
1. **Chat component** receives question → emits `chat:questionAsked`
2. **Avatar component** listens → transitions to `thinking` emotion (with question marks accent)
3. **Chat component** receives response → emits `chat:responseReceived`
4. **Avatar component** listens → transitions to `surprised` (with sparkles accent) then `happy` (no accent)
5. **Input component** ready → emits `chat:ready`
6. **Avatar component** listens → stays on `happy` (ready for next question)
7. **Error scenarios**: 
   - AI error or unclear question → `derp` (no accent)
   - Rate limit → `tired` (with Z's accent)
   - Offensive question → `annoyed` (with huff lines accent)

### Benefits of Event System
- **Modularity**: Each component is independent
- **Testability**: Easy to test components in isolation
- **Maintainability**: Changes to one component don't affect others
- **Extensibility**: Easy to add new components that listen to events
- **Flexibility**: Components can be rearranged without breaking communication
