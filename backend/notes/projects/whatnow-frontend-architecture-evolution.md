# WhatNow: Frontend Architecture Evolution

The WhatNow frontend has gone through significant evolution, from a quick vanilla JavaScript prototype to a professional React + TypeScript application with proper state management. This evolution demonstrates my ability to build projects iteratively, starting simple and progressing to production-quality architecture as requirements become clear.

The initial version was built with vanilla JavaScript, HTML, and CSS. No build tools, no frameworks, just straightforward DOM manipulation and fetch calls to the backend API. This was intentional - I wanted to prove the core concept worked before investing in framework complexity. The vanilla version had slider inputs for context selection, a button to generate recommendations, basic activity cards for display, and simple state management with global variables. It was functional but limited.

The decision to migrate to React came when the interaction complexity outgrew what was comfortable with vanilla JavaScript. Managing state across multiple interaction cycles (initial generation, marking favorites, regeneration, accumulation, final selection) was getting messy with manual DOM updates. React's component model and declarative rendering made that complexity manageable.

The React migration started with a straightforward translation - components that mostly matched the vanilla version's structure, but using React's state management and rendering. I built separate components for ContextSliders, ActivityCard, ActivityGrid, FavoritesPanel, and SessionManager. Each component had clear responsibilities and communicated through props and callbacks.

Adding TypeScript happened shortly after the React migration, motivated by catching bugs that type checking would have prevented. TypeScript interfaces for Activity, Context, SessionState, and API responses made the code more self-documenting and caught errors at compile time instead of runtime. The type safety especially helped when refactoring components, since the compiler immediately flagged everywhere that needed updates when interfaces changed.

Redux Toolkit was introduced when state management started feeling awkward with pure React state. The application needs to track current context, generated activities, marked favorites, accumulated favorites across multiple generations, selection history, and Session AI weights. Managing all that with useState and prop drilling was becoming unwieldy. Redux Toolkit provided a clean way to centralize that state with slices for sessionState, activities, and learning.

The state management architecture is interesting because it handles both UI state and AI learning state. The Session AI weights live in Redux and update after each selection, which means the frontend can immediately reflect updated recommendations without API calls. This gives instant feedback - I make a choice, the app immediately adjusts what it recommends, all client-side. Base AI updates happen on the backend after session completion, but Session AI is entirely frontend-based for responsiveness.

Styling evolved from plain CSS to Tailwind CSS. The utility-first approach made responsive design much easier, and the constraint of using predefined classes led to more consistent styling. Components like activity cards, sliders, and buttons have cohesive styling that adapts properly to mobile and desktop views without writing lots of custom media queries.

The component architecture follows patterns I learned from other projects. Components are small and focused - ActivityCard just renders one activity, ActivityGrid handles layout and mapping, ActivityInteraction orchestrates user choices. This composition makes the code easier to test and modify. When I wanted to change how activities are displayed, I only had to modify ActivityCard, and all uses of it updated automatically.

Error handling and loading states were gradual additions as edge cases revealed themselves in real usage. Loading spinners during API calls, error boundaries to catch rendering errors, graceful degradation when the backend is unreachable, and clear user feedback for all interaction states. These polish details make the difference between a prototype and a production application.

The build setup uses Vite for fast development and optimized production builds. Vite's hot module replacement makes development pleasant - changes appear instantly without full page reloads. The production build optimizes bundle size, eliminates dead code, and generates assets that load quickly even on slower connections.

One interesting technical decision was implementing Session AI learning directly in JavaScript rather than calling the backend for within-session updates. This meant translating the Python contextual bandit logic to JavaScript, ensuring mathematical equivalence between implementations. The benefit is zero-latency learning - recommendations improve immediately within the session without network roundtrips.

Testing strategy is admittedly minimal - I've relied mostly on real usage to validate behavior. For a personal project where I'm the only user, extensive unit tests felt like overengineering. But I did implement runtime validation that catches common errors like malformed API responses or invalid state transitions. In a team environment, I'd add proper unit tests for components and integration tests for user flows.

The evolution from vanilla JavaScript to React + TypeScript + Redux Toolkit demonstrates incremental improvement driven by actual needs. I didn't start with the full complexity because I didn't need it initially. As the application grew and requirements became clear, I added architectural sophistication where it provided genuine value. This is how real projects evolve - you don't build the perfect architecture upfront, you let it emerge from actual usage and requirements.

For employers, this shows I can build projects iteratively from simple to sophisticated, make strategic decisions about when to add framework complexity, handle full frontend application architecture including state management and TypeScript, and evolve codebases over time while maintaining functionality. The GitHub commit history shows this evolution clearly - you can trace how the project grew from simple to sophisticated while remaining functional at every stage.

