# moh-ami: French Learning Translation Tool

moh-ami (pronounced "moh-ah-mee", from "mot ami" meaning "word friend") is a French learning translation tool that I built to solve a personal challenge while demonstrating end-to-end LLM integration skills. It's a production-deployed application that goes beyond simple translation to provide detailed educational explanations for language learners.

The core concept is that simple translation tools don't help you understand why words are translated certain ways or what grammar rules apply. If you just see "Comment allez-vous?" translates to "How are you?", you don't learn why "allez" is used instead of "aller" or why "vous" can be formal "you" instead of plural. moh-ami provides word-by-word mappings, grammar rule explanations, cultural context notes, and alternative translations with explanations of differences.

I started this project while learning French myself and realizing that existing translation tools weren't helping me actually learn the language. I wanted to build something that explained the translation process, not just showed the result. This became an opportunity to demonstrate full-stack development with modern technologies and LLM integration in a production application.

The technical implementation uses Next.js 14 with the App Router, GraphQL API with Apollo Server, PostgreSQL database via Prisma ORM, and OpenAI GPT-4o-mini for the LLM integration. The frontend is React with TypeScript, Redux Toolkit for state management, and Tailwind CSS for styling. The system features synchronized side-by-side text comparison with interactive chunk selection, hover highlighting, and expandable explanation panels.

What makes moh-ami special is the structured LLM integration. I designed careful prompts that request specific JSON schema outputs, which makes the responses consistent and parseable. The system does semantic chunking where text is split into meaningful units (50-150 characters) rather than word-by-word, which produces more coherent explanations. There's validation logic that catches common LLM errors before they reach users, and comprehensive error handling for API failures, quota limits, rate limits, and context length issues.

The personal utility aspect is important - I actually use moh-ami when reading French text or practicing translations. Having an AI explain the grammar and context helps me learn more effectively than just seeing translations. This means the project provides genuine value beyond being a portfolio piece, which keeps me engaged with maintaining and improving it.

From a portfolio perspective, moh-ami demonstrates several valuable skills. It shows I can integrate LLMs into production applications with proper prompt engineering and error handling. It proves I understand full-stack development with modern frameworks like Next.js 14 and GraphQL. It shows I can design interactive user experiences with complex state management. Most importantly, it demonstrates I can build complete systems from concept to deployed application that solve real problems.

The project went through significant iteration during development. I started with complex text matching algorithms and simplified to ID-based chunk selection. I moved from eager to lazy initialization for OpenAI client to handle deployment compatibility. I evolved from generic prompts to structured JSON responses with validation. These pivots demonstrate adaptability and the ability to recognize when simpler approaches work better than complex ones.

What I'm particularly proud of is that moh-ami is real and deployed. You can visit the live application, enter text, and see it working. The source code is on GitHub showing the implementation details. This transparency means potential employers can verify everything I claim about the project by actually using it and reviewing the code.

