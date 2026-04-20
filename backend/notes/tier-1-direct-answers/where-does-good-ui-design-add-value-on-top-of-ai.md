# Where does good UI design add value on top of AI output?

Three of my projects show different shapes of this.

WhatNow gives activity recommendations, and users can set preferences with sliders — that's ordinary. The distinctive UI work is the card game: you repeatedly pick which of two options fits you better, and those pairwise choices are the training signal the model learns from. The mechanic turns training into something quick and playable on mobile so people keep supplying labels. Without it you don't have a collaborative learning loop, just filtered recommendations.

moh-ami is the opposite shape: the LLM produces detailed language explanations, but raw text would be unusable for learning. The UI adds side-by-side comparison, semantic chunks short enough to scan, hover highlighting between matching English and French phrases, and expandable panels for grammar and cultural context. The model output becomes something navigable rather than a wall of prose.

Folio is a third angle: the AI answers from notes, but the UI steers behaviour. Suggestion chips point at questions with strong coverage, scripted answers bypass the LLM for tight matches, and a layered fallback keeps the demo trustworthy for employers. The UI there is steering, safety rails, and recovery paths built on top of generation.

---

**shortTitle:** Where does UI add value on top of AI?
**emotion:** happy
**suggestions:**
- How do you handle unexpected AI output?
- How do you show AI uncertainty in a UI?
- What do you ask before building an AI UI?
- Tell me about WhatNow
- Tell me about moh-ami
- What is Folio?

**variants:**
- Where does a UI designer add value when there's AI behind the interface?
- What does UI do that AI can't?
- How do you make AI output more useful through interface design?
