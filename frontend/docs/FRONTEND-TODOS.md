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

- [ ] **Type Definitions**
  - **Test:** Shared TypeScript types are available for all components
  - **Verify:** Types can be imported and used across components, type safety is maintained
  - **Build:** Create `frontend/src/types/index.ts` with interfaces for Message, Suggestion, APIResponse, and other shared types

- [ ] **Header Component**
  - **Test:** Header displays name and "Get in Touch" link at top of page
  - **Verify:** Header renders with dark background (#2D4A42), name is visible, link navigates to contact page or section
  - **Build:** Create `frontend/src/components/Header.tsx` with dark header strip, name display, and "Get in Touch" link, styled with bg-header color

- [ ] **Avatar System**
  - **Test:** Avatar displays expressions and responds to events, accents animate independently
  - **Verify:** Avatar shows correct expression for each emotion, accents appear/disappear correctly, transitions are smooth
  - **Build:** Create avatar components that listen to events, render expressions from image assets, animate accents

  - [ ] **Avatar Core Components**
    - **Test:** Base face and accent components render correctly from image assets
    - **Verify:** Face expressions load from assets, accents overlay correctly, images are properly imported
    - **Build:** Create `frontend/src/components/AvatarFace.tsx` and `frontend/src/components/AvatarAccent.tsx` that render images from `frontend/src/assets/avatar/`

  - [ ] **FolioAvatar Component**
    - **Test:** Main avatar component listens to events and displays correct expression with accent
    - **Verify:** Avatar transitions between expressions on events, correct accent appears for each emotion, default state is 'happy'
    - **Build:** Create `frontend/src/components/FolioAvatar.tsx` that composes AvatarFace and AvatarAccent, listens to 'avatar:setEmotion' events, manages current expression state

  - [ ] **Avatar Animations**
    - **Test:** Accent animations work independently from face, animations are smooth
    - **Verify:** Question marks float/rotate, sparkles twinkle/pulse, Z's drift upward, huff lines puff briefly, face stays stable
    - **Build:** Add CSS animations or React animation library for accent animations (question marks, sparkles, zzz, huff)

  - [ ] **Avatar Event Integration**
    - **Test:** Avatar responds to all chat events correctly
    - **Verify:** 'chat:questionAsked' → thinking, 'chat:responseReceived' → surprised then happy, error events → appropriate error states
    - **Build:** Connect avatar to event bus, handle all event types, implement expression transition logic

- [ ] **Message Display**
  - **Test:** Single message bubble displays AI responses and updates when new response received
  - **Verify:** Message bubble shows current response, updates smoothly when new response arrives, empty state handled
  - **Build:** Create `frontend/src/components/MessageBubble.tsx` that listens to 'chat:responseReceived' events, displays message text, styled with ui-base color

  - [ ] **Message Bubble Component**
    - **Test:** Message bubble renders with correct styling and content
    - **Verify:** Background color is #F0F2F1, text color is #1E2A26, rounded corners, proper padding, content updates on events
    - **Build:** Create MessageBubble component with Tailwind classes using ui-base and primary-black colors, listens to event bus

  - [ ] **Message Content Handling**
    - **Test:** Message content displays correctly, empty state shows welcoming message
    - **Verify:** Text renders properly, empty state appears when no message, content transitions smoothly
    - **Build:** Implement message state management, empty state UI, content update logic

- [ ] **Input System**
  - **Test:** User can type questions and submit them, input emits events correctly
  - **Verify:** Input field accepts text, Enter key or button submits, 'chat:questionAsked' event is emitted, input clears after submit
  - **Build:** Create `frontend/src/components/InputBox.tsx` with text input, submit button, event emission, disabled state during processing

  - [ ] **Input Component**
    - **Test:** Input field is styled correctly and functional
    - **Verify:** Background color is #F0F2F1, text color is #1E2A26, input is accessible, submit works
    - **Build:** Create InputBox component with Tailwind styling, form handling, Enter key support

  - [ ] **Input Event Integration**
    - **Test:** Input emits correct events on submit and when ready
    - **Verify:** 'chat:questionAsked' emitted on submit, 'chat:ready' emitted when input is ready, events include question text
    - **Build:** Connect input to event bus, emit events with question data, handle submit logic

- [ ] **Suggestions System**
  - **Test:** Suggested questions appear in empty state and after responses, clicking fills input
  - **Verify:** Suggestions show when no question asked, suggestions appear after response, clicking suggestion submits question
  - **Build:** Create `frontend/src/components/FollowUpSuggestions.tsx` with suggestion chips, click handlers, conditional rendering

  - [ ] **Suggestions Component**
    - **Test:** Suggestions render with correct styling and are clickable
    - **Verify:** Background color is #5B8A7A, text color is #E8E8D8, chips are clickable, animations are smooth
    - **Build:** Create FollowUpSuggestions component with Tailwind styling using ui-secondary and primary-white colors

  - [ ] **Suggestions Logic**
    - **Test:** Suggestions appear at correct times and trigger input submission
    - **Verify:** Empty state suggestions show initially, follow-up suggestions show after response, clicking suggestion fills and submits input
    - **Build:** Implement suggestion state management, empty state detection, suggestion click handlers that emit events

- [ ] **API Integration**
  - **Test:** Mock API client simulates backend responses and emits events
  - **Verify:** API function accepts questions, returns responses after delay, emits 'chat:responseReceived' events, handles errors
  - **Build:** Create `frontend/src/api/chatApi.ts` with mock sendQuestion function, simulated delay, sample responses, event emission

  - [ ] **Mock API Client**
    - **Test:** Mock API returns responses based on questions or randomly
    - **Verify:** Function returns response object, delay is 1-2 seconds, response structure matches expected format
    - **Build:** Create chatApi.ts with async sendQuestion function, setTimeout for delay, mock response data

  - [ ] **API Event Integration**
    - **Test:** API client emits events when responses are received or errors occur
    - **Verify:** 'chat:responseReceived' emitted on success, 'chat:error' emitted on failure, events include response data
    - **Build:** Connect API client to event bus, emit events with response/error data, handle different response types

- [ ] **Landing Page**
  - **Test:** All components are composed together and work as integrated system
  - **Verify:** Header, Avatar, MessageBubble, InputBox, and FollowUpSuggestions all render and communicate via events
  - **Build:** Create `frontend/src/pages/LandingPage.tsx` that imports and composes all components, handles event flow

  - [ ] **Landing Page Layout**
    - **Test:** Landing page has correct layout with centered container
    - **Verify:** Container is max-width 600px, centered, padding 1rem, background extends full width
    - **Build:** Create LandingPage component with container div, Tailwind classes for layout, proper spacing

  - [ ] **Component Composition**
    - **Test:** All components are rendered in correct order and communicate
    - **Verify:** Header at top, Avatar and MessageBubble in middle, InputBox and Suggestions at bottom, events flow correctly
    - **Build:** Import all components, arrange in JSX, ensure event bus is shared across components

  - [ ] **Event Flow Integration**
    - **Test:** Complete event flow works from input to response to avatar updates
    - **Verify:** User submits question → avatar thinks → API responds → avatar surprised → avatar happy → suggestions appear
    - **Build:** Wire up complete event flow, connect API client to input, ensure all components respond to events

- [ ] **App Integration**
  - **Test:** App.tsx renders LandingPage instead of health check
  - **Verify:** LandingPage is displayed, old health check code is removed, app loads correctly
  - **Build:** Update `frontend/src/App.tsx` to import and render LandingPage, remove health check code

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

