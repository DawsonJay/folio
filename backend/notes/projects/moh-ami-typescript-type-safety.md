# moh-ami: TypeScript Implementation and End-to-End Type Safety

moh-ami is written entirely in TypeScript across frontend, API, and database layers. This demonstrates my proficiency with TypeScript and understanding of how type safety improves code quality, catches bugs early, and makes refactoring safer in production applications.

The type safety chain starts at the database with Prisma-generated types. The Prisma schema defines models (Translation, Chunk, WordMapping, User), and Prisma generates TypeScript interfaces matching these models. Every database query returns these typed objects. If you try to access `translation.invalidField`, TypeScript errors immediately because that field doesn't exist in the schema.

GraphQL types are defined in the schema and enforced by Apollo Server. The schema specifies types like `Translation`, `Chunk`, `Query`, `Mutation` with specific fields and their types. TypeScript generates types from the GraphQL schema through code generation tools. Resolvers must return objects matching these types, and TypeScript verifies the return values match what the schema promises.

Frontend types use the GraphQL schema types and component prop types. Apollo Client generates TypeScript types from GraphQL queries. When you query `translation { id, text, chunks { content } }`, Apollo generates an interface matching that exact query shape. React components use these types for props, ensuring data passed between components matches expectations.

Custom types handle business logic concerns. I defined types for ChunkData, WordMappingData, TranslationResult, and LLMResponse that represent internal data structures. These types aren't directly from the database or GraphQL but represent application concepts. Having explicit types for these makes the business logic code self-documenting and type-safe.

Utility types like Partial, Required, Pick, and Omit handle common type transformations. When the API returns full Translation objects but the UI only needs specific fields, `Pick<Translation, 'id' | 'text'>` creates a type with just those fields. When updating translations, `Partial<Translation>` makes all fields optional. These utility types reduce repetition and keep code DRY.

Strict TypeScript configuration enforces best practices. The tsconfig.json enables strict mode with noImplicitAny, strictNullChecks, strictFunctionTypes, and other strict options. This catches more potential bugs but requires more careful coding. The tradeoff is worthwhile - the compiler catches issues that would otherwise only surface at runtime.

Type guards provide runtime validation where needed. Functions like `isValidTranslation(data: unknown): data is Translation` check if runtime data matches expected types. This is crucial when parsing JSON from external APIs like OpenAI where TypeScript can't verify the response shape at compile time. Type guards bridge the gap between typed internal code and untyped external data.

Generic types make reusable components and functions type-safe. A generic error handler `handleError<T>(error: Error): Result<T>` works with any error type while preserving specific type information. Generic React components accept type parameters for props, making them reusable while maintaining type safety.

Discriminated unions handle complex state with precision. The loading state type `{ status: 'idle' } | { status: 'loading' } | { status: 'success', data: Translation } | { status: 'error', error: string }` precisely models all possible states. TypeScript narrows the type based on status checks, so accessing `data` when `status === 'success'` is type-safe, and accessing it otherwise is an error.

Interface vs type decisions follow community conventions. Interfaces for object shapes that might be extended, especially in public APIs. Type aliases for unions, intersections, and complex transformations. This isn't rigid but provides consistency that makes the codebase predictable.

The any type is avoided throughout the codebase except for legitimate unknown types from external sources. Instead of `any`, I use `unknown` when the type is genuinely unknown and validate with type guards. This maintains type safety while handling runtime data. Code reviews catch any instances of `any` and require justification or refactoring.

TypeScript with React uses modern patterns like functional components with generics for props. Component definitions like `const ChunkDisplay: React.FC<ChunkDisplayProps>` clearly indicate prop types. Hooks like useState and useEffect are properly typed so state updates and dependencies are verified. This prevents common React bugs like incorrect state updates or missing effect dependencies.

Async operations are typed with Promise<T>. API calls return Promise<Translation>, database queries return Promise<Translation | null>, and error handlers return Promise<Result<T>>. This makes async behavior explicit in types and helps catch issues like forgetting to await promises or incorrect error handling.

Enum types provide named constants with type checking. Language codes use an enum `enum Language { EN = 'en', FR = 'fr' }` rather than string literals. This prevents typos and makes valid values discoverable through autocomplete. TypeScript ensures you only pass valid Language values to functions expecting languages.

Mapped types handle repetitive type definitions. If multiple models share common fields like timestamps, a mapped type `WithTimestamps<T> = T & { createdAt: Date, updatedAt: Date }` adds those fields without repetition. This keeps types DRY and makes changes to common patterns easy.

The refactoring safety that TypeScript provides is invaluable. When I changed the chunk ID system from text-based to numeric IDs, TypeScript flagged every location that needed updating. Without types, this would require manually searching the codebase and testing extensively. With types, the compiler identifies every incompatible usage, and tests verify the refactored code works correctly.

IDE integration with TypeScript provides real-time feedback. VS Code (and Cursor) shows type errors inline, provides autocomplete based on types, shows parameter hints from function signatures, and enables safe refactoring tools like rename symbol. This tight integration makes development faster and less error-prone.

Type assertions are used sparingly and only when necessary. Sometimes you know more about a type than TypeScript can infer, like `const translation = data as Translation`. These are documented with comments explaining why the assertion is safe, and they're reviewed carefully because they bypass type checking.

What I learned from using TypeScript extensively is that the upfront cost of typing everything pays dividends throughout development. Bugs caught at compile time don't become production issues. Refactoring is safe and fast. The code is self-documenting through types. IDE features make development more productive. These benefits compound over time as the codebase grows.

For employers, the TypeScript implementation demonstrates I understand modern type system patterns, can implement end-to-end type safety across full-stack applications, use advanced TypeScript features appropriately, configure strict type checking, handle the boundaries between typed and untyped code safely, and appreciate how types improve code quality and maintainability. These skills are increasingly essential as TypeScript becomes the standard for JavaScript development.

