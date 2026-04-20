# Have you worked with a component library?

Material UI has been my primary component library for 5.5 years, across BriefYourMarket and then Nurtur. I've used it in the Nexus Dashboard, the Email Editor, and the Integrations Dashboard, so I know it well enough to know exactly what it's good for and where it fights back.

Nurtur didn't have a shared cross-project library, but individual projects would build their own set of wrapped MUI components — not usually changing the appearance much, but adding project-specific logic or combining standard components into more niche composites. That's a practical middle ground: you keep MUI's speed and built-in behaviour, but you get consistent API wrappers across your project.

The real trade-off with component libraries is granular visual control. For a functional UI where the design doesn't demand strict pixel precision, MUI is fast. But detailed custom designs often fight the library's defaults — overriding styles is friction, and if those overrides are frequent enough it's often cleaner to build from scratch. MUI form components are a good example of where the built-in logic genuinely earns its place: validation state, accessible labels, controlled inputs — that saves real time on standard pages.

---

**emotion:** happy
**suggestions:**
- What CSS frameworks have you used?
- How do you keep CSS manageable?
- Tell me about the Email Editor project
- Tell me about the Nexus Dashboard
- What state management libraries do you know?
- Tell me about your frontend experience?

**variants:**
- Have you worked with a design system?
- What component libraries are you familiar with?
- What's your experience with Material UI?
