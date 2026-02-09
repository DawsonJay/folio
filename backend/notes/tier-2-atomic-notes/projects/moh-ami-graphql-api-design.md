# moh-ami: GraphQL API Design and Implementation

The moh-ami backend uses GraphQL instead of REST, which was a deliberate architectural choice that demonstrates my understanding of modern API design patterns. GraphQL provides flexibility for the frontend to request exactly the data it needs, type safety through the schema, and a single endpoint for all operations.

I implemented the GraphQL server using Apollo Server, which integrates cleanly with Next.js. The setup involves defining a type schema that describes all available queries and mutations, creating resolver functions that implement the actual logic, and connecting to the PostgreSQL database through Prisma. Apollo Server handles the HTTP endpoint, query parsing, execution, and response formatting automatically.

The schema design reflects the domain model clearly. The main types are Translation (the result of translating text), Chunk (a semantic unit of translated text), WordMapping (connections between English and French words), and User (for potential future authentication). Each type has fields that make sense for the frontend's needs, with nullable fields where appropriate and required fields where data must always exist.

The query design focuses on the core use case - translating text. The main query is `translate(text: String!, sourceLanguage: String!, targetLanguage: String!): Translation!` which takes input text and returns a complete Translation object with all chunks, mappings, and explanations. This single query provides everything the frontend needs to render the translation interface, eliminating the multiple round-trips that REST APIs might require.

Mutations handle data modification operations. The primary mutation is `saveTranslation` which stores completed translations to the database for caching and history. This demonstrates CRUD operations in GraphQL and integration with Prisma for database persistence. Future mutations could handle user preferences, favorites, or feedback.

The resolver implementation is where business logic lives. Resolvers are functions that return data for each field in the schema. For the translate query, the resolver calls the OpenAI service to get translations, processes the LLM response into the schema format, validates the data, and returns the properly structured result. This separation between schema definition and implementation makes the code maintainable and testable.

Type safety was a major benefit of GraphQL. The schema acts as a contract between frontend and backend - if the frontend requests fields that don't exist or passes wrong parameter types, it fails at compile time (with TypeScript) or immediately on query execution. This catches bugs early compared to REST APIs where you might only discover issues at runtime when data doesn't match expectations.

Prisma integration handles database operations cleanly. Prisma generates TypeScript types from the database schema, so database queries are type-safe. The generated client provides methods like `prisma.translation.create()` and `prisma.translation.findMany()` that return properly typed objects. This end-to-end type safety from database to GraphQL to frontend eliminates entire classes of bugs.

One challenge was handling errors gracefully in GraphQL. Unlike REST where you use HTTP status codes, GraphQL always returns 200 OK with errors in the response body. I implemented proper error handling that distinguishes between user errors (invalid input), system errors (database failure), and external errors (OpenAI API failure). Each error type returns appropriate messages and allows the frontend to handle them differently.

The caching strategy leverages GraphQL's structure. Apollo Client on the frontend automatically caches query results based on query shape and parameters. This means if you translate the same text twice, the second request doesn't hit the backend. Combined with server-side database caching, this makes repeated translations nearly instant while keeping data fresh.

Performance considerations mattered for production deployment. GraphQL can suffer from the N+1 query problem where nested data causes multiple database queries. I used Prisma's include and select options to load related data in single queries. For translations with many chunks and mappings, this meant the difference between 1 database query versus potentially hundreds.

The development experience with GraphQL was excellent. Apollo provides GraphQL Playground in development mode, which is an interactive interface for testing queries and mutations. I could iterate on schema design, test resolvers, and debug issues without writing frontend code. This rapid feedback loop made development much faster than traditional API testing tools.

What I learned is that GraphQL adds complexity compared to simple REST APIs, but that complexity pays off for interactive applications with varying data needs. The type safety, flexible queries, and single endpoint made the frontend development significantly easier. For a portfolio project, it demonstrates I can work with modern API patterns beyond just REST.

For employers, the GraphQL implementation shows I understand API design principles, can work with sophisticated backend frameworks, implement type-safe systems end-to-end, and make architectural decisions based on project requirements rather than just using familiar patterns. These are skills that matter as teams adopt modern development practices.

