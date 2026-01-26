# Frontend Development Todos

- [x] **Event System**
  - **Test:** Components can communicate via centralized event bus without direct dependencies
  - **Verify:** Events can be emitted and listened to across different components, event bus instance is shared globally
  - **Build:** Create event bus class with on/emit/off methods, singleton instance, React hook wrapper

  - [x] **Event Type Definitions**
    - **Test:** TypeScript types exist for all event types and avatar emotions
    - **Verify:** AvatarEmotion, AccentType, and ChatEvent types are properly defined and exported
    - **Build:** Create `frontend/src/events/eventTypes.ts` with AvatarEmotion ('happy', 'thinking', 'surprised', 'derp', 'tired', 'annoyed'), AccentType ('questionMarks', 'sparkles', 'zzz', 'huff', null), and ChatEvent union types

  - [x] **Event Bus Implementation**
    - **Test:** Event bus can register listeners, emit events, and remove listeners
    - **Verify:** Multiple components can listen to same event, events are delivered to all listeners, listeners can be removed
    - **Build:** Create `frontend/src/events/eventBus.ts` with EventBus class using Map<EventType, Set<EventCallback>> for listeners, singleton instance exported

  - [x] **Event Bus React Hook**
    - **Test:** React components can use event bus via hook with automatic cleanup
    - **Verify:** Hook provides event bus instance, listeners are cleaned up on unmount, hook can be used in multiple components
    - **Build:** Create `frontend/src/hooks/useEventBus.ts` with useEvent and useEmit hooks that handle subscription and emission with automatic cleanup

- [x] **Type Definitions**
  - **Test:** Shared TypeScript types are available for all components
  - **Verify:** Types can be imported and used across components, type safety is maintained
  - **Build:** Create `frontend/src/types/index.ts` with interfaces for Message, Suggestion, APIResponse, and other shared types

- [x] **Header Component**
  - **Test:** Header displays name and "Reach Out" link at top of page
  - **Verify:** Header renders with dark background (#2D4A42), name is visible and clickable (links to home), link navigates to contact page, arrow has idle and hover animations
  - **Build:** Created `frontend/src/components/Header.tsx` with dark header strip, clickable name display, and "Reach Out" link with animated arrow icon, styled with bg-header color

- [x] **Avatar System**
  - **Test:** Avatar displays expressions and responds to events, accents animate independently
  - **Verify:** Avatar shows correct expression for each emotion, accents appear/disappear correctly, transitions are smooth
  - **Build:** Create avatar components that listen to events, render expressions from image assets, animate accents

  - [x] **Avatar Core Components**
    - **Test:** Base face and accent components render correctly from image assets
    - **Verify:** Face expressions load from assets, accents overlay correctly, images are properly imported
    - **Build:** Create `frontend/src/avatar/Avatar.tsx` and `frontend/src/avatar/Accent.tsx` that render images from `frontend/src/assets/avatar/`

  - [x] **FolioAvatar Component**
    - **Test:** Main avatar component listens to events and displays correct expression with accent
    - **Verify:** Avatar transitions between expressions on events, correct accent appears for each emotion, default state is 'happy'
    - **Build:** Created `frontend/src/avatar/Avatar.tsx` that composes face image and Accent component, listens to 'avatar:setEmotion' events, manages current expression state

  - [x] **Avatar Animations**
    - **Test:** Accent animations work independently from face, animations are smooth
    - **Verify:** Accents animate with diagonal movement and fade-out, face has cheerful rocking idle animation, animations are smooth
    - **Build:** Added CSS animations for accent (diagonal movement and fade-out) and avatar (rocking idle animation)

  - [x] **Avatar Event Integration**
    - **Test:** Avatar responds to all chat events correctly
    - **Verify:** 'chat:questionAsked' → thinking, 'chat:responseReceived' → surprised then happy, error events → appropriate error states
    - **Build:** Connected avatar to event bus, implemented emotion queue system with delay mechanism, handles all event types with appropriate emotion sequences

- [x] **Message Display**
  - **Test:** Single message bubble displays AI responses and updates when new response received
  - **Verify:** Message bubble shows current response, updates smoothly when new response arrives, empty state handled
  - **Build:** Created `frontend/src/components/ChatBubble.tsx` that listens to 'chat:responseReceived' events, displays message text, styled with ui-base color

  - [x] **Message Bubble Component**
    - **Test:** Message bubble renders with correct styling and content
    - **Verify:** Background color is #F0F2F1, text color is #1E2A26, rounded corners, proper padding, content updates on events
    - **Build:** Created ChatBubble component with Sass styling using ui-base and primary-black colors, listens to event bus, includes speech bubble point design

  - [x] **Message Content Handling**
    - **Test:** Message content displays correctly, empty state shows welcoming message
    - **Verify:** Text renders properly, empty state appears when no message, content transitions smoothly, scrolling works when content exceeds space
    - **Build:** Implemented message state management, initial welcome message, content update logic, height transitions, internal scrolling

- [x] **Input System**
  - **Test:** User can type questions and submit them, input emits events correctly
  - **Verify:** Input field accepts text, Enter key or button submits, 'chat:questionAsked' event is emitted, input clears when response received
  - **Build:** Created `frontend/src/components/InputBox.tsx` with text input, submit button with magnifying glass icon, event emission, event-driven disabled state, animations

  - [x] **Input Component**
    - **Test:** Input field is styled correctly and functional
    - **Verify:** Background color is #F0F2F1, text color is #1E2A26, accent-colored submit button with white icon, animations work, disabled state with grey shade
    - **Build:** Created InputBox component with Sass styling, form handling, Enter key support, magnifying glass icon with idle rock animation, hover effects, click spin animation

  - [x] **Input Event Integration**
    - **Test:** Input emits correct events on submit and responds to chat events
    - **Verify:** 'chat:questionAsked' emitted on submit, input disables on question asked, enables on response/error, input clears when response received
    - **Build:** Connected input to event bus, emits events with question data, listens to events for disabled state management, clears input on response

- [x] **Suggestions System**
  - **Test:** Suggested questions appear in empty state and after responses, clicking fills input
  - **Verify:** Suggestions show when no question asked, suggestions appear after response, clicking suggestion submits question
  - **Build:** Created `frontend/src/components/Suggestions.tsx` with suggestion chips, click handlers, conditional rendering, skeleton loaders

  - [x] **Suggestions Component**
    - **Test:** Suggestions render with correct styling and are clickable
    - **Verify:** Background color is #5B8A7A, text color is #E8E8D8, chips are clickable, animations are smooth
    - **Build:** Created Suggestions component with Sass styling using ui-secondary and primary-white colors, flex-wrap layout, varied skeleton loaders

  - [x] **Suggestions Logic**
    - **Test:** Suggestions appear at correct times and trigger input submission
    - **Verify:** Empty state suggestions show initially, follow-up suggestions show after response, clicking suggestion fills and submits input
    - **Build:** Implemented suggestion state management, loading state with skeletons, suggestion click handlers that emit events, input value population on suggestion click

- [x] **API Integration**
  - **Test:** API client connects to backend and emits events
  - **Verify:** API function accepts questions, returns responses after delay, emits 'chat:responseReceived' events, handles errors
  - **Build:** Created `frontend/src/api/chatApi.ts` with fetchInitialSuggestions and sendQuestion functions, `frontend/src/api/ChatApiClient.ts` singleton class that handles API calls via events

  - [x] **API Client Functions**
    - **Test:** API functions make HTTP requests to backend endpoints
    - **Verify:** Functions return response objects, handle errors, response structure matches expected format
    - **Build:** Created chatApi.ts with async fetchInitialSuggestions and sendQuestion functions, proper error handling, uses VITE_API_URL or vite proxy

  - [x] **API Event Integration**
    - **Test:** API client emits events when responses are received or errors occur
    - **Verify:** 'chat:responseReceived' emitted on success, 'chat:error' emitted on failure, events include response data
    - **Build:** Created ChatApiClient singleton class that listens to events, makes API calls, and emits responses via event bus

- [x] **Landing Page**
  - **Test:** All components are composed together and work as integrated system
  - **Verify:** Header, Avatar, ChatBubble, InputBox, and Suggestions all render and communicate via events
  - **Build:** Created `frontend/src/pages/LandingPage.tsx` that imports and composes all components, handles event flow

  - [x] **Landing Page Layout**
    - **Test:** Landing page has correct layout with centered container
    - **Verify:** Container is max-width 600px, centered, padding, background extends full width, avatar section expands to fill space, input at bottom
    - **Build:** Created LandingPage component with flexbox layout, avatar section uses flex: 1, input section pushed to bottom for mobile thumb access

  - [x] **Component Composition**
    - **Test:** All components are rendered in correct order and communicate
    - **Verify:** Header at top, Avatar and ChatBubble in middle, InputBox and Suggestions at bottom, events flow correctly
    - **Build:** Imported all components, arranged in JSX with proper sections, event bus shared across components

  - [x] **Event Flow Integration**
    - **Test:** Complete event flow works from input to response to avatar updates
    - **Verify:** User submits question → avatar thinks → API responds → avatar surprised → avatar happy → suggestions appear
    - **Build:** Wired up complete event flow, connected API client to input, all components respond to events, created INITIAL_SUGGESTIONS_RECEIVED event for clean separation

- [x] **App Integration**
  - **Test:** App.tsx renders LandingPage instead of health check
  - **Verify:** LandingPage is displayed, old health check code is removed, app loads correctly
  - **Build:** Updated `frontend/src/App.tsx` to import and render LandingPage, removed health check code, initialized ChatApiClient in main.tsx

- [ ] **Styling & Polish**
  - **Test:** All styling matches design specifications, responsive design works
  - **Verify:** Colors match palette, fonts load correctly, responsive design works on mobile and desktop, animations are smooth
  - **Build:** Verify CSS variables, font loading, Tailwind config, responsive breakpoints, animation performance

  - [ ] **Color Palette Verification**
    - **Test:** All colors match design specifications
    - **Verify:** Background colors (#1E2A26, #2D4A42), UI colors (#F0F2F1, #D4A574, #5B8A7A), text colors (#1E2A26, #E8E8D8) are correct
    - **Build:** Verify all Tailwind color classes and CSS variables match design specs

  - [ ] **Typography Verification**
    - **Test:** Fonts load correctly and are applied
    - **Verify:** Plus Jakarta Sans loads for body text, JetBrains Mono loads for code, font sizes match typography scale
    - **Build:** Verify font imports in index.css, check font-family classes, verify font-size usage

  - [ ] **Responsive Design**
    - **Test:** Layout works correctly on mobile and desktop
    - **Verify:** Container stays 600px max-width, elements maintain same size, background extends full width, no element stretching
    - **Build:** Test on mobile and desktop viewports, verify Tailwind responsive classes, check container behavior

  - [ ] **Animation Polish**
    - **Test:** All animations are smooth and performant
    - **Verify:** Avatar transitions are smooth, accent animations work, no jank or performance issues
    - **Build:** Optimize animations, use CSS transforms where possible, test performance, add transition timing

