# React Frontend Development Experience

I've been building React applications for over 3 years, and it's my primary framework for frontend development. My experience spans from small personal projects to enterprise-level applications at my current role at Nurtur, where I work as a Full Stack Developer.

I work exclusively with modern React patterns - functional components with Hooks, not class components. I'm very comfortable with the core Hooks like useState, useEffect, useContext, useMemo, and useCallback, and I understand when and why to use each one. I've built custom hooks to encapsulate reusable logic, like useScrollTracking for my portfolio's article navigation system and useDioramaAnimation for coordinating SVG animations.

TypeScript is my default choice for React projects now. I appreciate the type safety it provides, especially in larger applications where catching errors at compile time saves significant debugging time. I'm experienced with typing props, state, hooks, and event handlers. In my current Folio project, WhatNow frontend migration, and moh-ami, TypeScript has been essential for maintaining code quality.

For state management, I've used several approaches depending on project complexity. Context API with useContext for simpler apps like my portfolio website, Redux Toolkit for more complex applications like WhatNow and moh-ami, and component-level state when appropriate. I understand the tradeoffs between different state management approaches and can choose the right tool for the job.

Component architecture is something I think about carefully. I follow principles of composition over inheritance, building small, focused components that do one thing well. In my Integrations Dashboard at Nurtur, I created a component architecture that's been running in production for over 2 years with zero maintenance. For my portfolio website, I built a reusable article system with block components (TextBlock, CodeBlock, DemoBlock, TitleBlock) that compose together cleanly.

I'm experienced with React Router for single-page application navigation and have implemented complex routing patterns, including route-driven previews with URL state management in my portfolio. I understand how to handle navigation, protected routes, and dynamic routing based on data.

Performance optimization is something I've had to tackle in production. At Nurtur, I reduced a dashboard's load time from 15 seconds to under 5 seconds through strategic loading patterns, React Query caching, displaying counts before full objects, and implementing buffer systems. I understand concepts like memoization, lazy loading, code splitting, and when to optimize versus when premature optimization hurts development speed.

For styling, I've worked with several approaches: styled-components in my portfolio for component-scoped styles and theme integration, Tailwind CSS in WhatNow and moh-ami for utility-first styling, and Material UI (MUI) in the Nexus Dashboard at work for enterprise component libraries. I'm comfortable with CSS-in-JS, utility classes, and traditional CSS, and I can adapt to whatever approach a project uses.

I've worked with various React ecosystems and tools: Next.js for server-side rendering and App Router patterns in moh-ami, Vite for fast development builds in my portfolio and Folio projects, Create React App in earlier projects, and integration with GraphQL using Apollo Client for data fetching.

What I really value about React is how it scales from simple interfaces to complex applications while maintaining a consistent mental model. The component-based architecture feels natural to me, and the ecosystem of tools and libraries means I can solve almost any UI challenge. Whether I'm building smooth animations, complex forms, real-time data displays, or intricate layouts, React gives me the flexibility and power to create excellent user experiences.

