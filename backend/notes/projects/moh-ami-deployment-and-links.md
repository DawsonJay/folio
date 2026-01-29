# moh-ami: Deployment, Links, and Technical Stack

moh-ami is fully deployed and accessible as a production application. You can try the live system and explore the source code through these links:

**Live Application:** https://moh-ami-production.up.railway.app/

Visit the live app to experience the French learning translation tool in action. Type or paste English text, click translate, and see the detailed word-by-word mappings, grammar explanations, cultural context, and alternative translations. The interactive chunk selection and synchronized scrolling demonstrate the sophisticated UI patterns I implemented.

**Source Code:** https://github.com/DawsonJay/moh-ami

The GitHub repository contains the complete Next.js application including the frontend React components, GraphQL API implementation, Prisma database schema, OpenAI integration code, and deployment configuration. The code demonstrates modern full-stack development practices with TypeScript throughout, proper error handling, and production-ready patterns.

The technical stack represents modern web development best practices and demonstrates my proficiency with cutting-edge technologies:

**Frontend Technologies:**
- Next.js 14 with App Router for server-side rendering and optimal performance
- React 19 for the component-based UI with modern Hooks patterns
- TypeScript for type safety across the entire frontend codebase
- Redux Toolkit for centralized state management of complex interactions
- Tailwind CSS for utility-first responsive styling
- Apollo Client for GraphQL data fetching with automatic caching

**Backend Technologies:**
- Next.js API routes serving the GraphQL endpoint
- Apollo Server for GraphQL schema definition and resolver implementation
- Node.js runtime for server-side JavaScript execution
- Prisma ORM for type-safe database access and migrations
- PostgreSQL for relational data storage of translations and user data
- OpenAI GPT-4o-mini API for LLM-powered translations and explanations

**Deployment Platform:**
- Railway for both frontend and backend hosting
- Managed PostgreSQL database provided by Railway
- GitHub integration for automatic deployments on push
- Environment variable management through Railway dashboard
- SSL/HTTPS enabled by default for security

The choice of technologies reflects pragmatic decisions based on project requirements. Next.js 14 provides excellent developer experience with hot reload and automatic optimization. The App Router pattern is the modern Next.js approach replacing the older Pages Router. GraphQL provides flexibility for the frontend to request exactly what it needs. Prisma generates TypeScript types from the database schema for end-to-end type safety. Railway offers simple deployment with managed services.

The deployment process uses Railway's GitHub integration. When I push commits to the main branch, Railway automatically detects changes, builds the Next.js application, runs database migrations through Prisma, and deploys the updated version. This CI/CD pipeline means deployments happen automatically without manual intervention. Having this automated workflow is crucial for maintaining production applications.

Database management through Prisma provides clean migration workflows. Schema changes are defined in the Prisma schema file, migrations are generated with `prisma migrate dev`, and migrations are committed to git for version control. In production, Railway runs `prisma migrate deploy` automatically during deployment to update the database schema. This approach ensures database changes are tracked and reversible.

Environment configuration is handled through Railway's environment variables. The OpenAI API key, PostgreSQL connection string, and other secrets are configured through the Railway dashboard rather than committed to git. This follows security best practices by keeping sensitive credentials out of version control. The application loads these variables at runtime through Next.js's environment variable support.

Performance in production has been solid. The Next.js server-side rendering provides fast initial page loads. Apollo Client caching means repeated translations load instantly without API calls. The PostgreSQL database handles queries efficiently with proper indexing. The overall user experience is smooth with response times under 5 seconds for new translations and near-instant for cached results.

Monitoring and debugging in production uses Railway's built-in logging. I can view application logs, database connection status, and deployment history through the dashboard. When errors occur, the logs capture stack traces and context which helps diagnose issues. This observability is essential for maintaining production applications and responding to problems quickly.

The cost structure is reasonable for a portfolio project. Railway's free tier was sufficient initially, and the paid tier costs around $5/month for the resources moh-ami uses. OpenAI API costs are roughly $1-2/month based on my personal usage. The total cost of running moh-ami in production is under $10/month, which demonstrates that modern deployment platforms make production hosting affordable for individual developers.

What makes this deployment notable is that it's real and accessible. Employers can visit the URL, use the application, and see it working. They can review the GitHub repository and understand the implementation. This transparency proves the technical claims I make because everything is verifiable through live demonstration and code review.

The repository includes comprehensive README documentation with local development setup instructions, Docker Compose configuration for PostgreSQL, deployment procedures, and API documentation. This shows I understand that code is only part of the deliverable - documentation that helps others understand and contribute is equally important.

For employers evaluating moh-ami, the deployment demonstrates I can take applications from development to production, work with modern deployment platforms, implement proper CI/CD workflows, manage databases and migrations, handle environment configuration securely, and maintain production systems over time. These operational skills complement the development skills shown in the code itself.

