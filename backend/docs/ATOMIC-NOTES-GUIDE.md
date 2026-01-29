# Atomic Notes Writing Guide

A practical guide for creating embedding-optimized notes for the Folio RAG system.

## Introduction

Atomic notes are self-contained, semantically coherent chunks of information that form the knowledge base for the Folio chatbot. These notes are embedded using OpenAI's `text-embedding-3-small` model and stored in Pinecone, where they're retrieved based on semantic similarity to user questions.

The way you write these notes directly impacts how well the RAG system performs. Well-written notes lead to better retrieval, more accurate answers, and a superior user experience.

**Why this matters:** The LLM doesn't see all your notes at once. It only sees the 3-5 most relevant notes retrieved by the embedding system. If notes are poorly written, the right information might not be retrieved, or the LLM might struggle to synthesize a good answer.

For technical details on how embeddings and RAG work, see [ATOMIC-NOTES-TECHNICAL.md](ATOMIC-NOTES-TECHNICAL.md).

## Core Principles

### 1. Natural Language Over Structured Data

Embeddings work better with natural, conversational text than rigid structured formats.

**❌ Less Optimal:**
```markdown
# React Experience
Skill: React
Level: Advanced
Years: 3
Projects: Nexus, Folio
```

**✅ Better:**
```markdown
# React Frontend Development Experience

I have 3 years of professional experience with React, using it as my primary frontend framework for building interactive web applications. I've used React in production applications including Nexus Job Manager, where I built a complex job tracking interface with real-time updates, and Folio, my portfolio chatbot with smooth animations and dynamic UI components.
```

**Why:** Natural text captures relationships and context that embeddings can match to questions. The embedding model was trained on natural language, not structured data.

### 2. Include Synonyms and Related Terms

Explicitly mention alternative phrasings so the embedding captures different ways of asking the same question.

**✅ Good Example:**
```markdown
# Python Backend Development

I use Python for backend development, building REST APIs and web services. I work with FastAPI framework to create high-performance APIs, and I'm experienced with async programming, database integration using SQLAlchemy ORM, and building scalable backend architectures. I prefer Python for server-side development because of its readability and extensive ecosystem of libraries.
```

**Why it works:** Includes "backend development", "REST APIs", "web services", "server-side", "FastAPI", "SQLAlchemy" — different phrasings that map to similar questions.

### 3. Answer Likely Questions Directly

Structure notes to answer common questions people might ask.

**Common question types:**
- "What technologies do you know?"
- "What's your experience with [technology]?"
- "What projects have you worked on?"
- "How long have you been using [technology]?"
- "Why do you prefer [technology]?"

**✅ Good Structure:**
```markdown
# FastAPI Backend Experience

I've been building backend APIs with FastAPI for the past 2 years, using it as my primary framework for Python web development. FastAPI is my go-to choice for building REST APIs because of its automatic API documentation, type validation with Pydantic, and excellent async support.

I've used FastAPI in production applications including the Folio portfolio chatbot backend, where I integrated it with PostgreSQL, implemented RAG systems using LangChain, and built rate limiting with Redis. I'm experienced with async endpoints, dependency injection, middleware, and deploying FastAPI applications to production environments like Railway.

I prefer FastAPI over Flask or Django for API development because it's modern, fast, and has built-in support for async operations which is essential for AI-powered applications.
```

**Why:** Answers "what", "how long", "where used", "why" — covering multiple question angles in natural language.

### 4. Semantic Coherence (One Topic Per Note)

Each note should focus on one concept, technology, or project.

**❌ Too Broad:**
```markdown
# Full-Stack Development

I know React, Python, FastAPI, PostgreSQL, Redis, Docker, AWS, and many other technologies. I've worked on multiple projects and have experience with frontend, backend, databases, deployment, and DevOps.
```

**✅ Better (Split into Multiple Notes):**
```markdown
# React Frontend Development
[Focus on React specifically]

# Python Backend Development  
[Focus on Python/FastAPI specifically]

# Database Experience
[Focus on PostgreSQL/databases specifically]
```

**Why:** Focused notes match more precisely to specific questions. Broad notes dilute the embedding and may not rank highly for any specific topic.

### 5. Optimal Size: 200-500 Tokens

Notes should be long enough to provide context but focused enough to remain coherent.

- **Too short (< 100 tokens):** Lacks context, may not retrieve well
- **Too long (> 800 tokens):** Dilutes focus, increases noise, may exceed context limits
- **Just right (200-500 tokens):** Enough detail, maintains focus

**✅ Good Size Example (~350 tokens):**
```markdown
# PostgreSQL Database Experience

I've been working with PostgreSQL for 3 years, using it as my primary relational database for production applications. I'm experienced with SQLAlchemy ORM for database operations, designing schemas, writing complex queries, and optimizing database performance.

I've used PostgreSQL in several projects including the Nexus Job Manager where I designed the database schema for job tracking and user management, and the Folio chatbot backend where I store chat sessions, messages, and analytics events. I'm comfortable with migrations using Alembic, connection pooling, and working with JSON columns for flexible data storage.

I prefer PostgreSQL over MySQL or SQLite because of its advanced features, JSON support, and excellent performance for web applications. When designing databases, I focus on normalization, proper indexing, and query optimization to ensure the application scales well.
```

### 6. Self-Contained Context

Each note should make sense when retrieved alone. Don't assume other notes will be retrieved with it.

**❌ Requires External Context:**
```markdown
# React Project
Used it in the main project. Built the UI components with the patterns mentioned earlier.
```

**✅ Self-Contained:**
```markdown
# Nexus Job Manager - React Frontend

I built the frontend for Nexus Job Manager using React as the primary framework. This was a job tracking application where I implemented a microfrontend architecture, allowing different parts of the application to be developed and deployed independently.

I created reusable component libraries, implemented state management with React Context and React Query for server state, and built complex forms with validation. The application handles real-time job updates, user authentication, and responsive design for both desktop and mobile devices.

This project demonstrated my ability to architect scalable frontend applications and work with modern React patterns in a production environment.
```

**Why:** Standalone notes provide complete context without needing other notes. The LLM might only see this one note.

### 7. Overlapping Coverage Encouraged

Multiple notes can cover the same topic from different angles. This improves retrieval coverage.

**Example: React covered in multiple notes:**
```markdown
# React Experience
[Skill-focused: React as a skill, years of experience, general capabilities]

# Nexus Job Manager - React Implementation
[Project-focused: How React was used in this specific project]

# Frontend Architecture Patterns
[Pattern-focused: React patterns, component design, state management]
```

**Why:** Different angles match different question phrasings. Someone asking "What frontend frameworks do you know?" gets the skill note. Someone asking "Tell me about Nexus Job Manager" gets the project note.

### 8. Include Question-Like Phrases

Embeddings match better when notes include question-like language.

**✅ Good:**
```markdown
# Python Backend Development

I use Python for backend development, building APIs and web services. When people ask about my backend experience, I typically mention Python as my primary language. I've worked with Python for 3 years, and when asked about Python frameworks, I prefer FastAPI for modern API development because of its async support and automatic documentation.
```

**Why:** Phrases like "when people ask about", "I typically mention", "when asked about" align with question embeddings and improve retrieval.

### 9. Metadata for Filtering (Optional)

While the note content should be natural language, you can use Pinecone metadata for filtering.

**Structure in Pinecone:**
```python
{
    "id": "react-experience-001",
    "values": [0.023, -0.145, ...],  # embedding vector
    "metadata": {
        "type": "skill",           # For filtering: skill/project/experience
        "technology": "React",     # For filtering by technology
        "level": "advanced",       # For filtering by level
        "year": "2024",           # For temporal filtering
        "content": "I have 3 years..."  # Natural text for embedding
    }
}
```

**Why:** Metadata enables filtering (e.g., "only show skill notes" or "only show recent notes"), while natural content drives semantic matching.

## Note Structure Template

Use this template as a starting point for writing notes:

```markdown
# [Topic/Technology Name] - [Focus Area]

[Opening statement answering "what" - natural language, includes synonyms]
Example: "I have 3 years of professional experience with React, using it as my primary frontend framework for building interactive web applications."

[Experience details answering "how long" and "where used" - specific projects, years]
Example: "I've used React in production applications including Nexus Job Manager, where I built a complex job tracking interface, and Folio, my portfolio chatbot with smooth animations."

[Technical details answering "how" - specific skills, tools, patterns]
Example: "I'm experienced with React Hooks, Context API, React Query for data fetching, and React Router for navigation. I focus on component composition patterns and performance optimization."

[Context and preferences answering "why" - reasoning, comparisons]
Example: "I prefer React over Vue or Angular because of its flexibility, large ecosystem, and the way it encourages component-based thinking."

[Optional: Related topics - connections to other technologies/concepts]
Example: "I often pair React with TypeScript for type safety and use Vite as my build tool for fast development."
```

## Note Types

### Skill Notes

**Purpose:** Describe experience with a specific technology, tool, or skill.

**Focus on:**
- Years of experience
- Proficiency level
- Where/how you've used it
- Related technologies
- Why you prefer it

**Example:**
```markdown
# React Frontend Development Experience

I have 3 years of professional experience with React, using it as my primary frontend framework for building interactive web applications. When people ask about my frontend skills or what technologies I use for UI development, React is always at the top of my list.

I've used React in production applications including Nexus Job Manager, where I built a complex job tracking interface with real-time updates, and Folio, my portfolio chatbot with smooth animations and dynamic UI components. In these projects, I implemented React Hooks for state management, used Context API for global state, integrated React Query for server data fetching, and built routing with React Router.

I'm experienced with component composition patterns, creating reusable component libraries, and optimizing React applications for performance. I focus on building maintainable code with clear separation of concerns, using custom hooks to encapsulate logic, and implementing proper error boundaries.

I prefer React over Vue or Angular because of its flexibility, large ecosystem, and the way it encourages component-based thinking. When building user interfaces, React's declarative approach makes it easier to reason about complex UI state and interactions.
```

### Project Notes

**Purpose:** Describe a specific project, what was built, technologies used, and outcomes.

**Focus on:**
- What the project does
- Technologies used
- Your role/contributions
- Challenges solved
- Results/outcomes

**Example:**
```markdown
# Nexus Job Manager - Full-Stack Project

I built Nexus Job Manager as a full-stack job tracking application in 2024. This project helps teams manage job postings, track applicants, and coordinate hiring workflows. It was designed to handle hundreds of job postings and thousands of applicants efficiently.

The frontend was built with React and TypeScript, implementing a microfrontend architecture that allowed different parts of the application to be developed and deployed independently. I created a dashboard for job analytics, a real-time notification system, and complex filtering interfaces for applicant management.

The backend used Python with FastAPI, connected to a PostgreSQL database. I designed the database schema for job tracking and user management, implemented authentication and authorization with role-based access control, and built REST APIs for all CRUD operations. I used SQLAlchemy ORM for database interactions and Alembic for migrations.

The application handles real-time job updates using WebSockets, includes search functionality with full-text search, and processes applicant data with background tasks. I deployed the application to production using Docker containers, set up CI/CD pipelines, and implemented monitoring with logging and error tracking.

This project demonstrated my ability to architect and build full-stack applications from scratch, make technical decisions about architecture and technology choices, and deliver a production-ready system that scales.
```

### Experience Notes

**Purpose:** Describe work history, roles, responsibilities, and professional context.

**Focus on:**
- Role title and duration
- Responsibilities
- Technologies used
- Team size/structure
- Key achievements

**Example:**
```markdown
# Software Developer - Professional Experience

I've been working as a software developer for 3 years, building web applications and backend systems. My professional experience spans full-stack development, with a focus on building scalable, maintainable applications using modern technologies.

In my role as a developer, I've worked on projects ranging from small prototypes to large-scale production applications. I've built REST APIs using Python and FastAPI, created responsive frontend interfaces with React and TypeScript, and designed database schemas with PostgreSQL. I'm comfortable with the full development lifecycle, from requirements gathering and design to implementation, testing, and deployment.

I work with version control using Git, follow agile development methodologies, and practice test-driven development where appropriate. I've collaborated with teams using tools like GitHub, participated in code reviews, and contributed to technical documentation. I'm experienced with deployment workflows, using Docker for containerization and CI/CD pipelines for automated testing and deployment.

When people ask about my professional background or work experience, I highlight my ability to work independently on projects from conception to deployment, my focus on writing clean and maintainable code, and my experience with modern web development technologies and best practices.
```

## Writing Guidelines

### Do's

**Do use first person:**
✅ "I have 3 years of experience with React..."
❌ "James has 3 years of experience with React..."

**Reason:** The LLM responds as "I" (Folio speaking as James), so notes in first person integrate naturally.

**Do include years and dates:**
✅ "I've been working with Python for 3 years, starting in 2022..."
❌ "I've been working with Python for a while..."

**Reason:** Temporal information helps answer time-related questions.

**Do include comparisons:**
✅ "I prefer FastAPI over Flask because it has built-in async support..."
❌ "I use FastAPI..."

**Reason:** Comparisons help answer preference questions and show decision-making.

**Do mention related technologies:**
✅ "I use React with TypeScript, Vite for builds, and Tailwind for styling..."
❌ "I use React..."

**Reason:** Related technologies help the embedding connect to broader questions.

**Do write for humans:**
✅ "I built the Folio chatbot using React for the frontend and Python for the backend..."
❌ "Folio chatbot. Technologies: React (frontend), Python (backend)."

**Reason:** Natural language embeds better and synthesizes better.

### Don'ts

**Don't use structured data formats:**
❌ 
```markdown
Technology: React
Years: 3
Level: Advanced
```

**Don't assume other notes will be retrieved:**
❌ "As mentioned in my React experience note..."

**Don't be overly verbose:**
❌ 500+ words repeating the same information

**Don't use bullet points excessively:**
Use paragraphs for main content, bullets for lists only when appropriate.

**Don't include irrelevant information:**
Stay focused on one topic per note.

## Examples: Good vs Bad

### Example 1: Technology Experience

**❌ Bad:**
```markdown
# Technologies
React, Python, FastAPI, PostgreSQL, TypeScript, Docker, Git
```

**✅ Good:**
```markdown
# React Frontend Development Experience

I have 3 years of professional experience with React, using it as my primary frontend framework for building interactive web applications. I've used React in production applications including Nexus Job Manager and Folio, where I implemented complex user interfaces with real-time updates, smooth animations, and responsive design.

I'm experienced with modern React patterns including Hooks, Context API, custom hooks, and performance optimization techniques. I typically pair React with TypeScript for type safety, use Vite as my build tool, and integrate libraries like React Query for data fetching and React Router for navigation.
```

### Example 2: Project Description

**❌ Bad:**
```markdown
# Folio
Portfolio chatbot. React + Python. RAG system. Uses OpenAI.
```

**✅ Good:**
```markdown
# Folio - RAG-Powered Portfolio Chatbot

I built Folio as a minimalist portfolio website featuring an AI chatbot that answers questions about my skills, experience, and projects using Retrieval Augmented Generation (RAG). The name "Folio" references both portfolio and evokes growth, representing a living, evolving portfolio.

The frontend is built with React and TypeScript, featuring a single message bubble interface with smooth crossfade transitions, an animated avatar with emotion states, and an event-driven architecture for clean component communication. I implemented custom hooks for dynamic height constraints and used Sass for styling.

The backend uses Python with FastAPI, integrating LangChain for RAG orchestration, OpenAI's GPT-4o-mini for chat completion, and Pinecone as a vector database for semantic search. I designed an atomic notes system where knowledge is stored as semantically coherent chunks that are embedded and retrieved based on similarity to user questions. The system includes rate limiting, session management with compact context tracking, and analytics logging.

This project demonstrates my full-stack development capabilities, my understanding of modern AI/LLM technologies, and my ability to create polished, production-ready applications with attention to user experience.
```

### Example 3: Technical Skill

**❌ Bad:**
```markdown
# FastAPI
I know FastAPI. Used it in projects.
```

**✅ Good:**
```markdown
# FastAPI Backend Development

I've been building backend APIs with FastAPI for the past 2 years, using it as my primary framework for Python web development. FastAPI is my go-to choice for building REST APIs because of its automatic API documentation with OpenAPI, type validation using Pydantic, and excellent async support for high-performance applications.

I've used FastAPI in production applications including the Folio portfolio chatbot backend, where I built endpoints for chat interactions, integrated with PostgreSQL for data persistence, implemented rate limiting with Redis, and orchestrated RAG operations using LangChain. I'm experienced with async endpoints, dependency injection for database sessions, custom middleware, and deploying FastAPI applications to platforms like Railway.

I prefer FastAPI over Flask or Django for API development because it's modern, fast, and has built-in support for async operations which is essential for AI-powered applications that make external API calls. The automatic validation and documentation save development time and reduce bugs.
```

## Quick Reference Checklist

When writing a note, check that it has:

- [ ] **Natural language** throughout (not structured data)
- [ ] **First person** voice ("I have..." not "James has...")
- [ ] **200-500 tokens** (roughly 1-3 paragraphs)
- [ ] **One clear topic** (focused, not scattered)
- [ ] **Self-contained** context (makes sense alone)
- [ ] **Synonyms** and related terms included
- [ ] **Answers questions** directly ("what", "how long", "where", "why")
- [ ] **Years/dates** mentioned where relevant
- [ ] **Comparisons** or preferences included if applicable
- [ ] **Related technologies** mentioned to help connections
- [ ] **Specific examples** (projects, achievements, use cases)
- [ ] **Readable** by humans (not just optimized for machines)

## Next Steps

1. Read [ATOMIC-NOTES-TECHNICAL.md](ATOMIC-NOTES-TECHNICAL.md) to understand the technical foundation
2. Use the note structure template to write your first notes
3. Start with 5-10 notes covering your key skills and projects
4. Test retrieval with sample questions
5. Refine notes based on what gets retrieved and how well answers are generated

Remember: Notes are building blocks the LLM uses to construct answers. Write notes that work individually for retrieval and connect naturally for synthesis.

