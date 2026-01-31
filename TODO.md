# Project Todos

## Testing Issues
*Issues discovered during testing - to be fixed after testing phase*

- [x] **Typing animation in chat bubble**: When frontend is waiting for an API reply to a question, show a typing animation (3 dots that fade in and back out in sequence) in the chat bubble, like in typical chat applications

- [x] **Suggestion token limits**: Add limitations to the suggestions that the LLM returns:
  - Individual token limit per suggestion/question (45 characters)
  - Reason: If suggestions are too wide, they don't stack correctly on screen and are harder to display

- **Portfolio-focused suggestions**: Ensure all suggestions returned by the LLM are about James, his work, experience, and projects - not generic questions that could be asked of a search engine. All suggestions must revolve around the portfolio owner (James) and be specific to his background, skills, and work.

---

## Frontend Development

- [x] **Event System**
  - **Test:** Components can communicate via centralized event bus without direct dependencies
  - **Verify:** Events can be emitted and listened to across different components, event bus instance is shared globally
  - **Build:** Create event bus class with on/emit/off methods, singleton instance, React hook wrapper

  - [x] **Event Type Definitions**
    - **Test:** TypeScript types exist for all event types and avatar emotions
    - **Verify:** AvatarEmotion, AccentType, and ChatEvent types are properly defined and exported
    - **Build:** Create `frontend/src/events/eventTypes.ts` with AvatarEmotion ('happy', 'thinking', 'surprised', 'derp', 'tired', 'annoyed'), AccentType ('questionMarks', 'sparkles', 'zzz', 'huff', null), and ChatEvent union types

  - [x] **Event Bus Implementation**
    - **Test:** Event bus can register listeners, emit events, and remove listeners
    - **Verify:** Multiple components can listen to same event, events are delivered to all listeners, listeners can be removed
    - **Build:** Create `frontend/src/events/eventBus.ts` with EventBus class using Map<EventType, Set<EventCallback>> for listeners, singleton instance exported

  - [x] **Event Bus React Hook**
    - **Test:** React components can use event bus via hook with automatic cleanup
    - **Verify:** Hook provides event bus instance, listeners are cleaned up on unmount, hook can be used in multiple components
    - **Build:** Create `frontend/src/hooks/useEventBus.ts` with useEvent and useEmit hooks that handle subscription and emission with automatic cleanup

- [x] **Type Definitions**
  - **Test:** Shared TypeScript types are available for all components
  - **Verify:** Types can be imported and used across components, type safety is maintained
  - **Build:** Create `frontend/src/types/index.ts` with interfaces for Message, Suggestion, APIResponse, and other shared types

- [x] **Header Component**
  - **Test:** Header displays name and "Reach Out" link at top of page
  - **Verify:** Header renders with dark background (#2D4A42), name is visible and clickable (links to home), link navigates to contact page, arrow has idle and hover animations
  - **Build:** Created `frontend/src/components/Header.tsx` with dark header strip, clickable name display, and "Reach Out" link with animated arrow icon, styled with bg-header color

- [x] **Avatar System**
  - **Test:** Avatar displays expressions and responds to events, accents animate independently
  - **Verify:** Avatar shows correct expression for each emotion, accents appear/disappear correctly, transitions are smooth
  - **Build:** Create avatar components that listen to events, render expressions from image assets, animate accents

  - [x] **Avatar Core Components**
    - **Test:** Base face and accent components render correctly from image assets
    - **Verify:** Face expressions load from assets, accents overlay correctly, images are properly imported
    - **Build:** Create `frontend/src/avatar/Avatar.tsx` and `frontend/src/avatar/Accent.tsx` that render images from `frontend/src/assets/avatar/`

  - [x] **FolioAvatar Component**
    - **Test:** Main avatar component listens to events and displays correct expression with accent
    - **Verify:** Avatar transitions between expressions on events, correct accent appears for each emotion, default state is 'happy'
    - **Build:** Created `frontend/src/avatar/Avatar.tsx` that composes face image and Accent component, listens to 'avatar:setEmotion' events, manages current expression state

  - [x] **Avatar Animations**
    - **Test:** Accent animations work independently from face, animations are smooth
    - **Verify:** Accents animate with diagonal movement and fade-out, face has cheerful rocking idle animation, animations are smooth
    - **Build:** Added CSS animations for accent (diagonal movement and fade-out) and avatar (rocking idle animation)

  - [x] **Avatar Event Integration**
    - **Test:** Avatar responds to all chat events correctly
    - **Verify:** 'chat:questionAsked' → thinking, 'chat:responseReceived' → surprised then happy, error events → appropriate error states
    - **Build:** Connected avatar to event bus, implemented emotion queue system with delay mechanism, handles all event types with appropriate emotion sequences

- [x] **Message Display**
  - **Test:** Single message bubble displays AI responses and updates when new response received
  - **Verify:** Message bubble shows current response, updates smoothly when new response arrives, empty state handled
  - **Build:** Created `frontend/src/components/ChatBubble.tsx` that listens to 'chat:responseReceived' events, displays message text, styled with ui-base color

  - [x] **Message Bubble Component**
    - **Test:** Message bubble renders with correct styling and content
    - **Verify:** Background color is #F0F2F1, text color is #1E2A26, rounded corners, proper padding, content updates on events
    - **Build:** Created ChatBubble component with Sass styling using ui-base and primary-black colors, listens to event bus, includes speech bubble point design

  - [x] **Message Content Handling**
    - **Test:** Message content displays correctly, empty state shows welcoming message
    - **Verify:** Text renders properly, empty state appears when no message, content transitions smoothly, scrolling works when content exceeds space
    - **Build:** Implemented message state management, initial welcome message, content update logic, height transitions, internal scrolling

- [x] **Input System**
  - **Test:** User can type questions and submit them, input emits events correctly
  - **Verify:** Input field accepts text, Enter key or button submits, 'chat:questionAsked' event is emitted, input clears when response received
  - **Build:** Created `frontend/src/components/InputBox.tsx` with text input, submit button with magnifying glass icon, event emission, event-driven disabled state, animations

  - [x] **Input Component**
    - **Test:** Input field is styled correctly and functional
    - **Verify:** Background color is #F0F2F1, text color is #1E2A26, accent-colored submit button with white icon, animations work, disabled state with grey shade
    - **Build:** Created InputBox component with Sass styling, form handling, Enter key support, magnifying glass icon with idle rock animation, hover effects, click spin animation

  - [x] **Input Event Integration**
    - **Test:** Input emits correct events on submit and responds to chat events
    - **Verify:** 'chat:questionAsked' emitted on submit, input disables on question asked, enables on response/error, input clears when response received
    - **Build:** Connected input to event bus, emits events with question data, listens to events for disabled state management, clears input on response

- [x] **Suggestions System**
  - **Test:** Suggested questions appear in empty state and after responses, clicking fills input
  - **Verify:** Suggestions show when no question asked, suggestions appear after response, clicking suggestion submits question
  - **Build:** Created `frontend/src/components/Suggestions.tsx` with suggestion chips, click handlers, conditional rendering, skeleton loaders

  - [x] **Suggestions Component**
    - **Test:** Suggestions render with correct styling and are clickable
    - **Verify:** Background color is #5B8A7A, text color is #E8E8D8, chips are clickable, animations are smooth
    - **Build:** Created Suggestions component with Sass styling using ui-secondary and primary-white colors, flex-wrap layout, varied skeleton loaders

  - [x] **Suggestions Logic**
    - **Test:** Suggestions appear at correct times and trigger input submission
    - **Verify:** Empty state suggestions show initially, follow-up suggestions show after response, clicking suggestion fills and submits input
    - **Build:** Implemented suggestion state management, loading state with skeletons, suggestion click handlers that emit events, input value population on suggestion click

- [x] **API Integration**
  - **Test:** API client connects to backend and emits events
  - **Verify:** API function accepts questions, returns responses after delay, emits 'chat:responseReceived' events, handles errors
  - **Build:** Created `frontend/src/api/chatApi.ts` with fetchInitialSuggestions and sendQuestion functions, `frontend/src/api/ChatApiClient.ts` singleton class that handles API calls via events

  - [x] **API Client Functions**
    - **Test:** API functions make HTTP requests to backend endpoints
    - **Verify:** Functions return response objects, handle errors, response structure matches expected format
    - **Build:** Created chatApi.ts with async fetchInitialSuggestions and sendQuestion functions, proper error handling, uses VITE_API_URL or vite proxy

  - [x] **API Event Integration**
    - **Test:** API client emits events when responses are received or errors occur
    - **Verify:** 'chat:responseReceived' emitted on success, 'chat:error' emitted on failure, events include response data
    - **Build:** Created ChatApiClient singleton class that listens to events, makes API calls, and emits responses via event bus

- [x] **Landing Page**
  - **Test:** All components are composed together and work as integrated system
  - **Verify:** Header, Avatar, ChatBubble, InputBox, and Suggestions all render and communicate via events
  - **Build:** Created `frontend/src/pages/LandingPage.tsx` that imports and composes all components, handles event flow

  - [x] **Landing Page Layout**
    - **Test:** Landing page has correct layout with centered container
    - **Verify:** Container is max-width 600px, centered, padding, background extends full width, avatar section expands to fill space, input at bottom
    - **Build:** Created LandingPage component with flexbox layout, avatar section uses flex: 1, input section pushed to bottom for mobile thumb access

  - [x] **Component Composition**
    - **Test:** All components are rendered in correct order and communicate
    - **Verify:** Header at top, Avatar and ChatBubble in middle, InputBox and Suggestions at bottom, events flow correctly
    - **Build:** Imported all components, arranged in JSX with proper sections, event bus shared across components

  - [x] **Event Flow Integration**
    - **Test:** Complete event flow works from input to response to avatar updates
    - **Verify:** User submits question → avatar thinks → API responds → avatar surprised → avatar happy → suggestions appear
    - **Build:** Wired up complete event flow, connected API client to input, all components respond to events, created INITIAL_SUGGESTIONS_RECEIVED event for clean separation

- [x] **App Integration**
  - **Test:** App.tsx renders LandingPage instead of health check
  - **Verify:** LandingPage is displayed, old health check code is removed, app loads correctly
  - **Build:** Updated `frontend/src/App.tsx` to import and render LandingPage, removed health check code, initialized ChatApiClient in main.tsx

- [ ] **Styling & Polish**
  - **Test:** All styling matches design specifications, responsive design works
  - **Verify:** Colors match palette, fonts load correctly, responsive design works on mobile and desktop, animations are smooth
  - **Build:** Verify CSS variables, font loading, Tailwind config, responsive breakpoints, animation performance

  - [ ] **Color Palette Verification**
    - **Test:** All colors match design specifications
    - **Verify:** Background colors (#1E2A26, #2D4A42), UI colors (#F0F2F1, #D4A574, #5B8A7A), text colors (#1E2A26, #E8E8D8) are correct
    - **Build:** Verify all Tailwind color classes and CSS variables match design specs

  - [ ] **Typography Verification**
    - **Test:** Fonts load correctly and are applied
    - **Verify:** Plus Jakarta Sans loads for body text, JetBrains Mono loads for code, font sizes match typography scale
    - **Build:** Verify font imports in index.css, check font-family classes, verify font-size usage

  - [ ] **Responsive Design**
    - **Test:** Layout works correctly on mobile and desktop
    - **Verify:** Container stays 600px max-width, elements maintain same size, background extends full width, no element stretching
    - **Build:** Test on mobile and desktop viewports, verify Tailwind responsive classes, check container behavior

  - [ ] **Animation Polish**
    - **Test:** All animations are smooth and performant
    - **Verify:** Avatar transitions are smooth, accent animations work, no jank or performance issues
    - **Build:** Optimize animations, use CSS transforms where possible, test performance, add transition timing

---

## Backend Development

- [ ] **Database Models**
  - **Test:** SQLAlchemy models can be created, queried, and relationships work correctly
  - **Verify:** Models define correct table structure, relationships are properly configured, models can be imported and used
  - **Build:** Create SQLAlchemy models for chat sessions, messages, and analytics events with proper relationships

  - [ ] **Chat Session Model**
    - **Test:** Chat session can be created and retrieved with unique session ID
    - **Verify:** Model has id, session_id, created_at, updated_at fields, session_id is unique, relationships to messages work
    - **Build:** Create `backend/app/models/chat_session.py` with ChatSession model, SQLAlchemy columns, proper types

  - [ ] **Chat Message Model**
    - **Test:** Chat messages can be created and linked to sessions
    - **Verify:** Model has id, session_id (FK), question, answer, response_time_ms, timestamp fields, foreign key relationship works
    - **Build:** Create `backend/app/models/chat_message.py` with ChatMessage model, foreign key to ChatSession, proper relationships

  - [ ] **Analytics Event Model**
    - **Test:** Analytics events can be logged and queried
    - **Verify:** Model has id, session_id, event_type, data, timestamp fields, can store JSON data, queries work efficiently
    - **Build:** Create `backend/app/models/analytics_event.py` with AnalyticsEvent model, JSON column for event data

- [ ] **Database Migrations**
  - **Test:** Alembic can generate and apply migrations for all models
  - **Verify:** Migrations create tables correctly, relationships are established, migrations can be rolled back
  - **Build:** Set up Alembic, create initial migration, configure migration directory structure

  - [ ] **Alembic Setup**
    - **Test:** Alembic is configured and can generate migrations
    - **Verify:** `alembic init` works, alembic.ini is configured, migration directory exists
    - **Build:** Initialize Alembic in `backend/alembic/`, configure alembic.ini with database URL, set up env.py

  - [ ] **Initial Migration**
    - **Test:** Initial migration creates all tables correctly
    - **Verify:** Migration file is generated, tables match models, foreign keys are created, migration applies successfully
    - **Build:** Generate initial migration with `alembic revision --autogenerate`, review migration file, apply with `alembic upgrade head`

- [ ] **Pydantic Schemas**
  - **Test:** Request/response schemas validate data correctly
  - **Verify:** Schemas validate input types, return proper response formats, handle optional fields
  - **Build:** Create Pydantic models in `backend/app/schemas/` for API requests and responses

  - [ ] **Chat Schemas**
    - **Test:** Chat request and response schemas work for API endpoints
    - **Verify:** ChatRequest validates question string, ChatResponse includes answer and sources, optional fields handled
    - **Build:** Create `backend/app/schemas/chat.py` with ChatRequest, ChatResponse, SourceDocument schemas

  - [ ] **Session Schemas**
    - **Test:** Session schemas work for session management
    - **Verify:** SessionCreate, SessionResponse schemas validate correctly, optional fields work
    - **Build:** Create session-related schemas in `backend/app/schemas/session.py`

  - [ ] **Analytics Schemas**
    - **Test:** Analytics schemas validate event data
    - **Verify:** AnalyticsEvent schema validates event structure, optional fields work
    - **Build:** Create analytics schemas in `backend/app/schemas/analytics.py`

- [x] **OpenAI Service**
  - **Test:** OpenAI service can generate embeddings and chat completions
  - **Verify:** Embeddings are generated correctly, chat completions work, API keys are handled securely, errors are handled
  - **Build:** Create `backend/app/services/openai_service.py` with OpenAI client wrapper, embedding generation, chat completion

  - [x] **OpenAI Client Setup**
    - **Test:** OpenAI client initializes and authenticates correctly
    - **Verify:** API key is loaded from environment, client is initialized, connection works
    - **Build:** Set up OpenAI client with API key from environment variables, handle authentication errors

  - [x] **Embedding Generation**
    - **Test:** Service can generate embeddings for text
    - **Verify:** Embeddings are 1536 dimensions, model is text-embedding-3-small, embeddings are returned as arrays
    - **Build:** Implement embedding generation function using OpenAI embeddings API with text-embedding-3-small model

  - [x] **Chat Completion**
    - **Test:** Service can generate chat responses using gpt-4o-mini
    - **Verify:** Responses are generated, model is gpt-4o-mini, temperature is set correctly, errors are handled
    - **Build:** Implement chat completion function using OpenAI chat API with gpt-4o-mini model, proper prompt formatting

- [ ] **Pinecone Service**
  - **Test:** Pinecone service can connect, upsert vectors, and query similar vectors
  - **Verify:** Connection to Pinecone works, vectors can be upserted, queries return similar vectors, index exists
  - **Build:** Create `backend/app/services/pinecone_service.py` with Pinecone client, upsert, and query functions

  - [ ] **Pinecone Client Setup**
    - **Test:** Pinecone client connects to index correctly
    - **Verify:** API key is loaded, index name is configured, connection is established
    - **Build:** Set up Pinecone client with API key and index name from environment variables

  - [ ] **Vector Upsert**
    - **Test:** Service can upsert vectors with metadata to Pinecone
    - **Verify:** Vectors are stored, metadata is preserved, IDs are unique, upsert succeeds
    - **Build:** Implement upsert function that takes vectors, IDs, and metadata, stores in Pinecone index

  - [ ] **Vector Query**
    - **Test:** Service can query for similar vectors
    - **Verify:** Queries return top-k similar vectors, metadata is included, results are sorted by similarity
    - **Build:** Implement query function that takes query vector, returns top-k results with metadata

- [x] **RAG Service**
  - **Test:** RAG service can retrieve relevant context and generate answers using LangChain
  - **Verify:** Questions retrieve relevant notes, context is included in prompt, LLM generates answers, sources are returned
  - **Build:** Create `backend/app/services/rag_service.py` with LangChain RAG chain, retrieval, and answer generation

  - [x] **LangChain Setup**
    - **Test:** LangChain components are configured correctly
    - **Verify:** OpenAIEmbeddings is initialized, Pinecone vector store is connected, LLM is configured
    - **Build:** Set up LangChain with OpenAIEmbeddings, Pinecone vector store, ChatOpenAI with gpt-4o-mini

  - [x] **Retrieval Chain**
    - **Test:** Retrieval chain retrieves relevant documents and generates answers
    - **Verify:** Top 3-5 relevant chunks are retrieved, context is included in prompt, answer is generated, sources are tracked
    - **Build:** Create RetrievalQA chain with LangChain, configure retriever with top-k=5, set up prompt template

  - [x] **Prompt Template**
    - **Test:** Prompt template includes context and generates first-person responses
    - **Verify:** Template includes retrieved context, question, and instructions for first-person voice, prompt is formatted correctly
    - **Build:** Create prompt template with context placeholder, question placeholder, first-person instructions

  - [x] **Source Tracking**
    - **Test:** RAG service returns source documents with answers
    - **Verify:** Source documents are included in response, metadata is preserved, sources are relevant
    - **Build:** Configure RetrievalQAWithSourcesChain or track sources manually, return sources with answer

- [ ] **Context Manager**
  - **Test:** Context manager maintains compact context per session and updates it
  - **Verify:** Context is created per session, updated after exchanges, included in prompts, stays within token limits
  - **Build:** Create `backend/app/services/context_manager.py` with context creation, update, and retrieval functions

  - [ ] **Context Storage**
    - **Test:** Compact context can be stored and retrieved per session
    - **Verify:** Context is stored in memory or database, retrieved by session ID, structure is maintained
    - **Build:** Implement context storage (in-memory dict or database), context structure with topics, projects, interests

  - [ ] **Context Update**
    - **Test:** Context can be updated after each exchange
    - **Verify:** New information is added, context stays compact, irrelevant info is pruned, update is efficient
    - **Build:** Implement context update logic that extracts key information from exchange, updates context structure

  - [ ] **Context Integration**
    - **Test:** Compact context is included in RAG prompts
    - **Verify:** Context is added to prompt template, doesn't exceed token limits, enhances response quality
    - **Build:** Integrate context manager with RAG service, include context in prompt template

- [ ] **Rate Limiter**
  - **Test:** Rate limiter enforces multi-tier limits per IP address
  - **Verify:** 5 per minute, 50 per hour, 100 per day limits are enforced, IP addresses are tracked, limits reset correctly
  - **Build:** Create `backend/app/services/rate_limiter.py` with Redis or in-memory rate limiting, multi-tier checks

  - [ ] **Rate Limit Storage**
    - **Test:** Rate limit data can be stored and retrieved efficiently
    - **Verify:** Timestamps are stored per IP, lookups are fast, old entries are cleaned up, Redis or Map works
    - **Build:** Set up Redis client or in-memory Map for storing rate limit timestamps, implement cleanup logic

  - [ ] **Multi-tier Checks**
    - **Test:** All three rate limits are checked on each request
    - **Verify:** Minute, hour, and day limits are all checked, first violation blocks request, limits are independent
    - **Build:** Implement check_rate_limit function that checks all three tiers, returns limit status and message

  - [ ] **Rate Limit Messages**
    - **Test:** Rate limit errors include conversion opportunity message
    - **Verify:** Error message includes limit type, suggests contact for interview, HTTP 429 status code
    - **Build:** Format rate limit error messages with limit type and contact suggestion, return 429 status

- [x] **Atomic Notes Knowledge Base**
  - **Test:** Atomic notes can be loaded, embedded, and stored in vector database
  - **Verify:** Notes are loaded from markdown files, embedded correctly, stored in Pinecone, can be retrieved
  - **Build:** Create note loading system, embedding pipeline, and Pinecone upsert process

  - [x] **Note Loading**
    - **Test:** Markdown notes can be loaded from directory
    - **Verify:** Notes are read from `backend/data/notes/`, parsed correctly, metadata is extracted, structure is maintained
    - **Build:** Create note loader that reads markdown files, parses content, extracts metadata (type, topics)

  - [x] **Note Embedding**
    - **Test:** Notes can be embedded and prepared for vector storage
    - **Verify:** Notes are embedded using OpenAI, embeddings are 1536 dimensions, metadata is preserved
    - **Build:** Implement embedding pipeline that embeds note content, creates vector IDs, prepares metadata

  - [x] **Vector Database Population**
    - **Test:** Notes can be upserted to Pinecone index
    - **Verify:** All notes are stored, vectors are searchable, metadata is preserved, upsert is idempotent
    - **Build:** Create script or function to upsert all notes to Pinecone, handle errors, verify completion

- [x] **Chat API Endpoint**
  - **Test:** Chat endpoint accepts questions and returns answers with RAG system
  - **Verify:** POST /api/chat accepts question, returns answer with suggestions, uses RAG system, errors are handled
  - **Build:** Created `backend/app/api/chat.py` with RAG-powered chat endpoint, Pydantic models, confidence threshold routing, profanity filtering

  - [x] **Chat Endpoint Implementation**
    - **Test:** Endpoint handles chat requests correctly
    - **Verify:** Request validation works, response is formatted, status codes are correct, RAG system is integrated
    - **Build:** Created POST /api/chat endpoint with Pydantic request/response models, RAG integration, confidence threshold routing

  - [x] **Initial Suggestions Endpoint**
    - **Test:** Endpoint returns initial suggestions for users to start conversations
    - **Verify:** GET /api/suggestions returns 6 starter questions, delays 1 second, response format matches frontend types
    - **Build:** Created GET /api/suggestions endpoint with 1 second delay, recruiter-focused initial suggestions matching frontend format

  - [ ] **Session Management**
    - **Test:** Chat endpoint creates and manages sessions
    - **Verify:** Sessions are created on first request, session ID is returned, messages are linked to sessions
    - **Build:** Implement session creation logic, session ID generation, session storage in database

  - [ ] **Error Handling**
    - **Test:** Endpoint handles errors gracefully
    - **Verify:** Rate limit errors return 429, API errors are caught, error messages are user-friendly, logging works
    - **Build:** Add try/except blocks, error response formatting, proper HTTP status codes, error logging

  - [ ] **Response Formatting**
    - **Test:** Responses include answer, sources, and metadata
    - **Verify:** Response JSON includes answer text, source documents, session ID, response time
    - **Build:** Format response with ChatResponse schema, include all required fields, calculate response time

- [ ] **Analytics Logging**
  - **Test:** Analytics events are logged for all chat interactions
  - **Verify:** Questions are logged, responses are logged, timestamps are recorded, session IDs are tracked
  - **Build:** Create analytics logging system that records events to database, includes all required fields

  - [ ] **Event Logging**
    - **Test:** Analytics events can be logged to database
    - **Verify:** Events are created with correct data, stored in database, queries work, performance is acceptable
    - **Build:** Implement logging function that creates AnalyticsEvent records, stores in database, handles errors

  - [ ] **Chat Analytics Integration**
    - **Test:** Chat endpoint logs analytics events
    - **Verify:** Question events are logged, response events are logged, timestamps are accurate, data is complete
    - **Build:** Integrate analytics logging into chat endpoint, log question and response events

  - [ ] **Analytics Data Structure**
    - **Test:** Analytics events store all required data
    - **Verify:** Full question text, response, timestamp, session ID, response time, IP address are stored
    - **Build:** Ensure AnalyticsEvent model and logging function capture all required analytics fields

- [x] **API Routes**
  - **Test:** All API routes are registered and accessible
  - **Verify:** Routes are mounted correctly, CORS is configured, routes return correct responses
  - **Build:** Set up FastAPI router structure, mount API routes, configure CORS middleware

  - [x] **Router Setup**
    - **Test:** API routers are organized and mounted correctly
    - **Verify:** Chat router is mounted, analytics router is mounted, routes are accessible, structure is clean
    - **Build:** Create router structure in `backend/app/api/`, mount routers in main.py, organize routes logically

  - [x] **CORS Configuration**
    - **Test:** CORS allows frontend to make requests
    - **Verify:** Frontend origin is allowed, preflight requests work, credentials are handled
    - **Build:** Configure CORS middleware in main.py with frontend origin, allow methods and headers

- [x] **Environment Configuration**
  - **Test:** Environment variables are loaded and validated
  - **Verify:** Required variables are present, optional variables have defaults, validation works, .env.example is complete
  - **Build:** Set up environment variable loading, validation, create .env.example with all required variables

  - [x] **Environment Variables**
    - **Test:** All required environment variables are defined
    - **Verify:** DATABASE_URL, OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME are set, optional vars have defaults
    - **Build:** Document all environment variables in .env.example, add validation in main.py or config module

  - [x] **Configuration Management**
    - **Test:** Configuration is loaded and accessible throughout application
    - **Verify:** Config values are loaded from environment, can be imported, defaults work, validation errors are clear
    - **Build:** Create config module or use python-dotenv, load and validate configuration, provide defaults

- [ ] **Error Handling & Logging**
  - **Test:** Application handles errors gracefully and logs appropriately
  - **Verify:** Errors are caught, logged with context, user-friendly messages are returned, logging is configured
  - **Build:** Set up logging configuration, add error handlers, create error response schemas, add logging throughout

  - [ ] **Logging Setup**
    - **Test:** Application logs events and errors correctly
    - **Verify:** Logs are written, log levels are appropriate, format is readable, errors include stack traces
    - **Build:** Configure Python logging, set log levels, format log messages, add logging to key functions

  - [ ] **Error Handlers**
    - **Test:** Global error handlers catch and format errors
    - **Verify:** Unhandled exceptions are caught, error responses are formatted, status codes are correct, errors are logged
    - **Build:** Add FastAPI exception handlers, format error responses, log errors with context

- [ ] **Testing & Validation**
  - **Test:** Critical functionality can be tested
  - **Verify:** Tests can be written and run, test database can be used, mocking works, test coverage is reasonable
  - **Build:** Set up testing framework (pytest), create test database setup, add example tests for key functions

  - [ ] **Test Setup**
    - **Test:** Testing framework is configured and can run tests
    - **Verify:** pytest is installed, test directory exists, tests can be discovered and run, fixtures work
    - **Build:** Install pytest, create tests directory, add pytest.ini or pyproject.toml config, create test fixtures

  - [ ] **Key Function Tests**
    - **Test:** Critical functions have basic tests
    - **Verify:** RAG service can be tested, rate limiter can be tested, API endpoints can be tested
    - **Build:** Add example tests for RAG service, rate limiter, API endpoints with mocking

