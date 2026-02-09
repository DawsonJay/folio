# Tell me about moh-ami

moh-ami (pronounced "moh-ah-mee", from "mot ami" meaning "word friend") is a French learning translation tool that I built to solve a personal challenge while demonstrating end-to-end LLM integration skills. It's a production-deployed application that goes beyond simple translation to provide detailed educational explanations for language learners.

The core concept is that simple translation tools don't help you understand why words are translated certain ways or what grammar rules apply. If you just see "Comment allez-vous?" translates to "How are you?", you don't learn why "allez" is used instead of "aller" or why "vous" can be formal "you" instead of plural. moh-ami provides word-by-word mappings, grammar rule explanations, cultural context notes, and alternative translations with explanations of differences.

I started this project while learning French myself and realizing that existing translation tools weren't helping me actually learn the language. I wanted to build something that explained the translation process, not just showed the result. This became an opportunity to demonstrate full-stack development with modern technologies and LLM integration in a production application.

What makes moh-ami special to me is the direct personal connection - I was solving a real problem for someone I care about, which gave the work genuine meaning beyond just building something for my portfolio. The tool has been shared with friends learning French, and their feedback validated the educational value. Knowing real people find it useful beyond just being a portfolio piece makes the project more meaningful.

The technical implementation uses Next.js 14 with the App Router, GraphQL API with Apollo Server, PostgreSQL database via Prisma ORM, and OpenAI GPT-4o-mini for the LLM integration. The frontend is React with TypeScript, Redux Toolkit for state management, and Tailwind CSS for styling. The system features synchronized side-by-side text comparison with interactive chunk selection, hover highlighting, and expandable explanation panels.

What makes moh-ami special is the structured LLM integration. I designed careful prompts that request specific JSON schema outputs, which makes the responses consistent and parseable. The system does semantic chunking where text is split into meaningful units (50-150 characters) rather than word-by-word, which produces more coherent explanations. There's validation logic that catches common LLM errors before they reach users, and comprehensive error handling for API failures, quota limits, rate limits, and context length issues.

The project was built over approximately 3-4 weeks of focused development, with the initial implementation happening in a single intensive session on January 11, 2026. This rapid development timeline demonstrates I can deliver complete, deployed applications in reasonable timeframes rather than spending months on perfect implementations. Balancing quality with delivery speed matters in professional contexts.

Operating moh-ami costs under $10 per month - about $5 for Railway hosting and $1-2 for OpenAI API usage based on my personal usage patterns. This proves I understand cost implications of technical decisions and can build efficient systems.

---

**emotion:** happy
**suggestions:**
- How do you approach AI system design?
- What challenges have you faced?
- Tell me about your LLM experience
- How do you ensure AI system quality?
- What AI technologies are you learning?
- What projects have you built?

