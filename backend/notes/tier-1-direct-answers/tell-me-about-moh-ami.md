# Tell me about moh-ami

moh-ami (from "mot ami" meaning "word friend") is a French learning tool with production LLM integration. It goes beyond simple translation to provide word-by-word mappings, grammar explanations, cultural context, and alternative translations. Simple translators don't teach you why translations work.

I built this solving a personal challenge learning French. Existing tools showed "Comment allez-vous?" translates to "How are you?" but didn't explain why "allez" is used or why "vous" can be formal. I wanted something that explained the process, not just the result.

The technical stack uses Next.js 14 App Router, GraphQL API with Apollo Server, PostgreSQL via Prisma ORM, and OpenAI GPT-4o-mini. Frontend is React/TypeScript with Redux Toolkit and Tailwind CSS. Features synchronized side-by-side text comparison with interactive chunk selection and expandable explanation panels.

The LLM integration uses structured prompt engineering. I designed prompts requesting specific JSON schemas, making responses consistent and parseable. The system does semantic chunking - splitting text into meaningful units 50-150 characters rather than word-by-word for more coherent explanations. Validation logic catches common LLM errors before reaching users, with comprehensive error handling for API failures, quota limits, and rate limits.

Built and deployed in a single intensive session January 11, 2026 - from scratch to production-ready in one day. Operating costs are minimal - about $1-2 monthly for OpenAI API usage, with hosting on Railway covered by a £5/month subscription that hosts all my projects.

---

**emotion:** happy
**suggestions:**
- How do you approach AI system design?
- How do you approach technical debt?
- Tell me about your LLM experience
- How do you ensure AI system quality?
- What AI technologies are you learning?
- What projects have you built?

