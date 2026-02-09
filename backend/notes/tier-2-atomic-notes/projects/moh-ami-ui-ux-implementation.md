# moh-ami: UI/UX Design and Interactive Implementation

The moh-ami user interface was designed to make language learning intuitive and engaging through interactive elements, synchronized scrolling, and careful information architecture. The challenge was presenting complex grammatical information without overwhelming users while maintaining a clean, accessible design.

The core layout uses a side-by-side comparison view with English text on the left and French translation on the right. This parallel presentation lets users see both languages simultaneously, which is crucial for understanding translations. The layout is responsive - on mobile it stacks vertically, on tablet and desktop it shows side-by-side. This required careful CSS and component design to maintain functionality across screen sizes.

Synchronized scrolling was one of the most challenging features to implement correctly. When you scroll the English text, the French text scrolls proportionally to keep corresponding sections aligned. This isn't simple one-to-one scrolling because English and French text don't have identical heights - French often runs longer due to grammar. I calculate scroll percentages and apply them proportionally, which keeps things roughly aligned even when text heights differ.

The chunk selection system provides interactivity that makes the tool engaging. Text is divided into semantic chunks (phrases or sentences), and clicking any chunk highlights it and shows detailed explanations in an expandable panel. Hover effects provide visual feedback so users know chunks are interactive. This chunked approach is much more usable than word-by-word selection which would feel tedious and disconnected.

The ID-based chunk system was a simplification from my original complex approach. Initially I tried matching chunks by text content and character positions, which was fragile and broke when text had small variations. I switched to giving each chunk a unique ID, and both English and French chunks with the same ID are treated as pairs. This is simpler, more reliable, and easier to debug.

Explanation panels expand below selected chunks showing word-by-word mappings, grammar rules, cultural context, and alternative translations. The panels use smooth CSS transitions for expansion and collapse, which feels polished. Information is organized hierarchically with clear headings so users can quickly scan for the details they want. This progressive disclosure pattern keeps the interface clean while providing depth when needed.

The hover highlighting provides immediate visual feedback. When you hover over an English chunk, the corresponding French chunk highlights too, and vice versa. This helps users understand which sections correspond without clicking. The highlighting uses subtle color changes and border styling rather than aggressive effects, which keeps it professional and readable.

State management with Redux Toolkit handles the complex interaction patterns. The application needs to track which chunk is selected, scroll positions for synchronization, expanded explanation panels, loading states during translation, error states from API failures, and translation history. Redux centralizes this state and makes the component logic simpler. Each component focuses on rendering rather than managing complex state.

The loading experience matters for perceived performance. Translating text takes 2-4 seconds due to LLM processing time. I show a loading indicator with a progress message, disable the input during processing, and provide visual feedback that work is happening. This prevents users from thinking the app froze and manages expectations about wait times.

Error handling in the UI needs to be informative without being alarming. Network errors show a friendly message about checking connection. API quota errors explain the limitation and suggest trying later. Validation errors highlight the specific problem (like text too long) and suggest fixes. Each error type gets appropriate messaging rather than generic "something went wrong" alerts.

The color scheme uses Tailwind CSS with a clean, modern palette. I chose blue tones for primary actions, gray for secondary elements, and warm colors for highlights. The typography is carefully sized with good contrast ratios for accessibility. Line height and letter spacing are tuned for readability since users will be reading detailed explanations.

Mobile responsiveness required specific considerations beyond just stacking layouts. Touch targets are sized appropriately for fingers rather than mouse pointers. Synchronized scrolling feels natural with touch gestures. Explanation panels expand smoothly without jumping the viewport. The interface degrades gracefully on small screens by simplifying rather than breaking.

One UX detail I'm proud of is the empty state design. Before any translation, the interface shows helpful examples of what you can do, rather than just blank boxes. This guides new users and makes the purpose immediately clear. Good empty states make interfaces more discoverable and less intimidating.

The performance optimization includes lazy loading of explanation panels (they're not rendered until expanded), debouncing of scroll events for synchronization (prevents excessive calculations), memoization of expensive computations in React, and efficient Redux selectors that only trigger re-renders when relevant state changes. These optimizations keep the interface smooth even with complex interactions.

What I learned from this implementation is that good UI/UX is about thoughtful details stacked together. Synchronized scrolling alone isn't impressive, but combined with chunk selection, hover highlighting, smooth animations, good error handling, and careful state management, it creates a polished experience. Each detail is straightforward, but the combination makes the tool feel professional.

For employers, the UI implementation demonstrates I can build complex interactive interfaces with React, implement sophisticated UX patterns like synchronized scrolling and progressive disclosure, manage complex application state with Redux, and think about user experience details that make applications pleasant to use. These skills matter for building products users actually want to use.

