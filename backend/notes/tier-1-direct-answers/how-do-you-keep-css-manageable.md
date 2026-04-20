# How do you keep CSS manageable?

In professional settings I've mostly worked with Material UI and styled-components, which keeps CSS co-located with the component that uses it. That turns out to be a natural enforcement mechanism: if a component's styles are getting unwieldy, it's a concrete signal that the component is trying to do too much and needs to be split. The file size acts as a pressure valve.

For projects using pure CSS or Sass I define a rigid structure from the start: a style file sitting next to each component file in the codebase, shared styles at the root level in a styles folder, split across separate files for animations, fonts, global styles and variables, all linked through an index. Each piece stays small for the same reason as styled-components — scope limits complexity.

The BriefYourMarket legacy codebase was a useful lesson in what happens without that structure. The CSS was far past saving. My approach there was surgical: make the minimum change needed, don't add to the damage, and accept that the only real fix was a full rewrite. Some codebases you manage, and some you contain.

---

**emotion:** thinking
**suggestions:**
- What CSS frameworks have you used?
- Have you worked with a component library?
- How do you approach technical debt?
- When do you refactor versus rewrite?
- Tell me about your frontend experience?
- How do you approach an unfamiliar codebase?

**variants:**
- How do you structure CSS in a large project?
- How do you organise CSS as a project grows?
- How do you stop CSS becoming a mess?
