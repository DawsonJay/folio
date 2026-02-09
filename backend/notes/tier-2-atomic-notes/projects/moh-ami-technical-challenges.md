# moh-ami: Technical Challenges and Solutions

Building moh-ami involved solving numerous technical challenges across LLM integration, frontend complexity, and production deployment. The solutions I developed demonstrate problem-solving abilities and the practical engineering skills needed for production applications.

**Challenge: Reliable LLM Output Parsing**

The core challenge was getting consistent, parseable output from GPT-4o-mini. LLMs are probabilistic and sometimes return malformed JSON, missing fields, or unexpected formats. Users can't see raw API errors - the system needs to work reliably.

Solution: Structured prompt engineering that requests specific JSON schema with example outputs. Temperature set to 0.3 for consistency while maintaining natural explanations. Validation logic that strips markdown code blocks (when LLM wraps JSON), corrects index mismatches in word mappings, provides default values for missing optional fields, and retries with adjusted prompts when responses are unusable. This defensive approach handles LLM unreliability gracefully.

**Challenge: Semantic Text Chunking**

Initially I tried word-by-word translation, but explanations felt disconnected because words lack phrase-level context. English "Comment allez-vous" needs to be explained as a greeting phrase, not three separate words.

Solution: Semantic chunking algorithm that groups text into meaningful units of 50-150 characters. This is roughly phrase or sentence level. The LLM explains "Comment allez-vous?" as a complete unit rather than "Comment" (what), "allez" (go), "vous" (you) separately. The chunked approach produces more coherent, useful explanations while maintaining reasonable API token usage.

**Challenge: Synchronized Scrolling with Variable Heights**

English and French text don't have identical heights - French often runs 10-20% longer due to grammar. Simple one-to-one scrolling doesn't work because corresponding sections end up misaligned.

Solution: Proportional scroll synchronization using percentage-based calculations. When English text scrolls to 40% of its height, French text scrolls to 40% of its height. This maintains approximate alignment even when absolute heights differ. Debouncing scroll events prevents excessive calculations. The implementation feels natural and keeps corresponding sections visible together.

**Challenge: Complex State Management**

The application tracks selected chunks, scroll positions, expanded panels, loading states, error states, translation history, and user preferences. Managing this with component state was becoming unwieldy.

Solution: Redux Toolkit for centralized state management with clean slices for each concern. translationSlice handles translations and chunks, uiSlice manages selections and expanded panels, errorSlice tracks error states. Components connect to Redux and focus on rendering rather than complex state logic. This separation makes the code maintainable and predictable.

**Challenge: Lazy Initialization for Deployment**

During Next.js build time, environment variables might not be available, so eagerly creating the OpenAI client failed builds. The deployment process kept breaking with "API key not found" errors.

Solution: Lazy initialization pattern where the OpenAI client is created on first use rather than at import time. The service exports a function that checks if the client exists, creates it if needed, then returns it. This ensures the client is only created at runtime when environment variables are definitely available. Small change, big impact on deployment reliability.

**Challenge: Cost Management**

LLM API calls cost money. At $0.15 per million tokens, each translation costs $0.001-0.003. Without optimization, costs could add up quickly.

Solution: Database caching of completed translations using PostgreSQL and Prisma. If the same text is requested again, return the cached result instead of calling OpenAI. Semantic chunking reduces token usage compared to word-by-word approaches. Text length limits prevent expensive translations of extremely long texts. These optimizations keep costs manageable while maintaining full functionality.

**Challenge: Error Handling for External APIs**

OpenAI API calls can fail in many ways: quota exceeded, billing problems, rate limits, network failures, timeout errors, context length exceeded. Each failure mode needs specific handling.

Solution: Comprehensive error handling with specific logic for each error type. Quota errors show user-friendly messages about limits. Rate limit errors implement exponential backoff and retry. Network failures have timeout and retry logic. Context length errors suggest breaking text into smaller chunks. Each error provides actionable feedback rather than generic failures.

**Challenge: Chunk Selection with Complex Text**

Initially I tried matching chunks by text content, which broke when LLM slightly paraphrased or when text had special characters. The mapping between English and French chunks was fragile.

Solution: ID-based chunk system where each chunk gets a unique identifier. English chunks and French chunks with the same ID are treated as pairs. This is much simpler and more reliable than text matching. IDs are generated sequentially and embedded in the chunk metadata. Selection, highlighting, and explanation display all use IDs rather than text matching.

**Challenge: Mobile Responsiveness**

The side-by-side layout with synchronized scrolling and interactive chunks needed to work on mobile devices with completely different interaction patterns (touch vs mouse, small screens).

Solution: Responsive design that stacks layouts vertically on mobile rather than side-by-side. Touch targets sized appropriately for fingers (minimum 44x44px). Scroll synchronization works with touch gestures. Explanation panels expand without jumping viewport using careful CSS. The interface degrades gracefully on small screens by simplifying rather than breaking.

**Challenge: GraphQL N+1 Query Problem**

Loading translations with all chunks and word mappings could trigger hundreds of database queries - one for the translation, one per chunk, one per word mapping. This was slow and inefficient.

Solution: Prisma's include and select options to eagerly load related data in single queries. Instead of separate queries for each relationship, one query loads translation with all chunks and mappings together. This reduced database queries from potentially hundreds to one, dramatically improving API response time.

Each challenge represents a point where the project could have stalled or produced poor results. The fact that moh-ami works reliably in production means I successfully navigated all these technical obstacles. More importantly, I did it in ways that are maintainable, understandable, and follow best practices rather than quick hacks.

For employers, these challenge-solution pairs demonstrate I don't just write code that works in development - I build systems that handle real-world complexity, external API unreliability, performance requirements, and cost constraints. These problem-solving skills across the full stack are what enable taking projects from concept to production.

