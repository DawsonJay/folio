# WhatNow: Deployment, Links, and Technical Stack

WhatNow is fully deployed and accessible as a production application. You can try the live system and explore the source code through these links:

**Live Application:** https://whatnow-frontend.onrender.com

Visit the live app to experience the contextual bandit recommendation system in action. Select your current context using sliders for mood, energy level, social preference, available time, and weather conditions. The AI generates 50 personalized activity suggestions, you pick your favorites, regenerate if needed, and make a final selection. The system learns from your choices to improve future recommendations.

**Frontend Repository:** https://github.com/DawsonJay/whatnow-frontend

The frontend is built with React, TypeScript, Redux Toolkit, and Tailwind CSS. The repository shows the complete evolution from vanilla JavaScript to professional TypeScript architecture, implementing the Session AI learning system directly in the browser for immediate responsiveness. The code demonstrates modern React patterns, proper TypeScript typing, clean component architecture, and Redux state management.

**Backend Repository:** https://github.com/DawsonJay/whatnow-backend

The backend uses FastAPI with Python, PostgreSQL for data persistence, and implements the Base AI with online learning capabilities. The repository contains the contextual bandit implementation, activity database with semantic embeddings, user preference tracking, and API endpoints for recommendations and feedback. It demonstrates production-quality Python backend development with proper async handling, database integration, and AI model serving.

The technical stack reflects pragmatic decisions based on deployment constraints and project requirements:

**Frontend Technologies:**
- React 18 for UI components and state management
- TypeScript for type safety and better development experience  
- Redux Toolkit for centralized state management of session and selections
- Tailwind CSS for responsive styling with utility classes
- Session AI implemented in JavaScript for zero-latency response

**Backend Technologies:**
- FastAPI for high-performance Python API with automatic OpenAPI documentation
- PostgreSQL for reliable data persistence of activities, users, and preferences
- Custom contextual bandit implementation (lightweight, no TensorFlow/PyTorch)
- Semantic embeddings (384 dimensions) generated via sentence transformers
- Base AI with configurable learning rate for long-term preference modeling

**Deployment Platform:**
- Frontend deployed on Render (static site hosting)
- Backend deployed on Render (Python service)
- PostgreSQL hosted on Render's managed database service
- Migrated from Railway due to platform constraints and pricing changes

The choice of technologies was driven by finding the right balance between capability and constraints. I originally used heavier ML libraries like scikit-learn and TensorFlow, but deployment limitations pushed me toward custom lightweight implementations. This turned out to be beneficial - the custom code is easier to understand, faster to execute, and more flexible for my specific use case than general-purpose ML libraries would have been.

The deployment on Render has been stable and reliable. The frontend serves globally with good performance, the backend handles API requests efficiently, and the PostgreSQL database maintains data integrity across restarts and updates. Having a live, publicly accessible deployment means potential employers can actually try the system and see it working, not just read about it or watch videos.

What makes this deployment notable is that it's a complete system, not a prototype. It handles user accounts, persists data across sessions, implements proper error handling, provides responsive feedback, and continues learning from real usage. The fact that I use it myself means it's been battle-tested with real interactions over time.

The repositories demonstrate clean code organization, proper Git practices with meaningful commit messages, documentation of setup and deployment procedures, and evolution of the project through multiple iterations. The commit history tells the story of technical decisions and pivots - moving from metadata to embeddings, vanilla JavaScript to TypeScript, Railway to Render - showing how real projects evolve to meet changing requirements and constraints.

For employers evaluating WhatNow, the live application and source code provide complete transparency into my capabilities. You can see the working system, review the code quality and architecture, examine technical decisions and their reasoning, and understand how I approach production deployment. This combination of live demo and open source code removes any ambiguity about what I'm capable of building.

