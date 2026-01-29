# moh-ami: Database Design and Prisma Implementation

The database layer in moh-ami demonstrates modern ORM usage with Prisma, type-safe database operations, and practical schema design for a production application. Prisma generates TypeScript types from the database schema which provides end-to-end type safety from database to API to frontend.

The database schema is defined in Prisma's schema language which is clean and declarative. The main models are User (for authentication, currently minimal), Translation (storing completed translations), Chunk (the semantic text units), and WordMapping (connections between source and target words). Each model has appropriate relationships - Translation has many Chunks, Chunk has many WordMappings - which Prisma handles through foreign key relations.

Field types are carefully chosen. String fields for text content with appropriate length constraints. DateTime fields with @default(now()) for automatic timestamps. Enum types for fixed value sets like language codes (EN, FR, ES, etc). Optional vs required fields use nullable modifiers to express the schema's intent clearly. This declarative approach makes the schema readable and maintainable.

Prisma migrations manage schema changes over time. During development, `prisma migrate dev` generates migration files that capture schema changes as SQL statements. These migrations are committed to git for version control. In production, `prisma migrate deploy` applies pending migrations. This workflow ensures database changes are tracked, reversible, and applied consistently across environments.

The generated Prisma Client provides type-safe database access with excellent TypeScript integration. Operations like `prisma.translation.create()`, `prisma.translation.findMany()`, `prisma.translation.update()` return properly typed objects matching the schema models. If you try to access fields that don't exist or pass wrong parameter types, TypeScript catches it at compile time before the code ever runs.

Query patterns in moh-ami leverage Prisma's relation loading capabilities. The `include` option eagerly loads related data - `prisma.translation.findUnique({ include: { chunks: true, wordMappings: true } })` loads a translation with all its chunks and mappings in a single query. This prevents the N+1 query problem where you'd otherwise make separate queries for each relationship.

The `select` option optimizes queries by loading only needed fields. If the API only needs translation IDs and text but not full chunk data, `select: { id: true, text: true }` loads just those fields. This reduces data transfer and speeds up queries by avoiding unnecessary field loading.

Database indexing ensures query performance. Primary keys get automatic indexes. Foreign keys that are queried frequently (like translation_id on chunks) have explicit indexes defined in the schema. Unique constraints on fields that must be unique (like user email) provide both data integrity and query optimization. Prisma generates appropriate SQL indexes from these schema annotations.

The caching strategy uses the database as a simple cache for translations. When text is translated, the result is stored in PostgreSQL. Subsequent requests for the same text query the database first - if found, return the cached result instead of calling OpenAI. This dramatically reduces API costs and speeds up repeated translations from seconds to milliseconds.

Error handling for database operations is important in production. Connection failures, constraint violations, query timeouts, and transaction failures all need specific handling. Prisma throws specific error types for different failure modes. The GraphQL resolvers catch these errors and return appropriate messages rather than exposing raw database errors to clients.

The PostgreSQL choice provides ACID transactions, robust querying, and reliable data persistence. For moh-ami's needs - storing translations with related chunks and mappings - a relational database makes sense. Prisma abstracts the SQL complexity while still providing access to PostgreSQL's power when needed through raw queries.

Migration rollback is possible through Prisma's migration system. If a migration causes problems in production, you can revert to the previous schema version. This safety net is crucial for production applications where database changes carry risk. The migration files are version controlled, so rolling back code also rolls back database schema.

The development workflow with Prisma is smooth. Schema changes in the `.prisma` file, run `prisma migrate dev` to generate migration and update types, and TypeScript immediately reflects the new schema. The generated types update automatically, so your IDE provides accurate autocompletion and type checking based on the current database schema. This tight integration makes database development fast and safe.

Seeding data for development uses Prisma's seeding functionality. A seed script creates sample translations, users, and related data for testing. This ensures development databases have realistic data rather than starting empty. Seeders are idempotent - you can run them multiple times without creating duplicate data.

One challenge was handling nullable relations in TypeScript. Prisma marks optional relations as potentially undefined, which is correct but requires null checking throughout the code. I handled this with TypeScript's optional chaining and nullish coalescing operators. Functions that expect related data include type guards to ensure data exists before accessing it.

The Prisma Studio tool provides a visual interface for exploring database contents during development. You can view, edit, and delete records through a web UI without writing SQL queries. This is incredibly helpful for debugging and understanding data state during development.

Connection pooling is handled automatically by Prisma in production. The database connection is established once and reused across requests rather than creating new connections for each query. This improves performance and reduces database server load, which matters as request volume scales.

What I learned from implementing the database layer is that modern ORMs like Prisma eliminate much of the tedious SQL writing while preserving type safety and performance. The generated TypeScript types prevent entire classes of bugs. The migration system makes schema evolution manageable. These tools make database development feel like an integrated part of the application rather than a separate concern.

For employers, the Prisma implementation demonstrates I can design appropriate database schemas, use modern ORMs effectively, implement type-safe database access, manage migrations and schema evolution, optimize query performance, and handle production database concerns like connection pooling and error handling. These skills are essential for backend development in modern full-stack applications.

