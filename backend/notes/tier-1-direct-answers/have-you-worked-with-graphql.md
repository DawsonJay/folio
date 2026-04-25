# Have you worked with GraphQL?

Yes — moh-ami is built on GraphQL throughout. I used Apollo Server for the backend API and Apollo Client for frontend data fetching with automatic caching.

The reason I chose GraphQL over REST for that project was the data shape. moh-ami is a French learning translation tool, and the translation data has complex relationships — text segments, their translations, associated grammar notes, difficulty levels. With REST I'd either over-fetch (send everything and filter client-side) or build multiple endpoints for different views. GraphQL let the frontend request exactly what each component needed in a single query, which kept both the API and the frontend logic clean.

The implementation involved defining the schema first, then writing resolvers that mapped to the Prisma database layer. Working with TypeScript throughout meant the schema types and the client code stayed in sync — if a field changed in the schema, the TypeScript compiler flagged every place it was used. That's the version of GraphQL that's worth using; without type safety it's hard to justify the added complexity over REST.

---

**emotion:** happy
**suggestions:**
- Tell me about moh-ami
- What's your backend development experience?
- How do you ensure code quality?
- What's your biggest weakness?
- What's your experience with REST APIs?
- What databases have you worked with?
