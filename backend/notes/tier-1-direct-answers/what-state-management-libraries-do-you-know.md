# What state management libraries do you know?

Redux Toolkit is my primary state management library — I've used it in the Email Editor at Nurtur, moh-ami, and WhatNow. The Email Editor was a good case for it: a four-person team working on complex, interconnected state across a drag-and-drop editor. RTK's slice pattern gave everyone a clear place to put state logic and made it predictable to trace what was happening when something went wrong.

For server state, React Query is what I reach for — I used it heavily on the Nexus Dashboard for caching and preventing redundant API calls. React Query and Redux complement each other well: Redux for client-side application state, React Query for data fetched from the server.

For simpler needs, local component state with `useState` and `useContext` is usually the right answer. The temptation to reach for global state management too early creates more complexity than it solves — I try to start local and only lift state when it actually needs to be shared.

---

**emotion:** happy
**suggestions:**
- Tell me about your experience with React
- Tell me about the Email Editor project
- Tell me about moh-ami
- Tell me about WhatNow
- How do you ensure code quality?
- Tell me about the Nexus Dashboard
