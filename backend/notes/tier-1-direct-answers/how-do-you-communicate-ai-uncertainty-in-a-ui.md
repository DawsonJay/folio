# How do you communicate AI confidence scores or uncertainty in a UI without losing user trust?

It depends on what the AI is for and what the user's relationship with it is meant to be.

On WhatNow the model produces activity recommendations and the user trains it over time with pairwise choices — picking which of two options fits better. A low confidence score there isn't a frustrating error, it's part of the loop. I reframed it as the user and AI being on the same side, improving together. Uncertainty could be surfaced openly because the user had agency over it — a low score just meant the next choices would help.

Folio is the opposite context. It's a professional showcase and its job is to communicate competence. I only flag uncertainty when confidence falls below the threshold for reliable matching: at that point it returns a clear message that there isn't enough material and suggests alternative questions. Outside that band I make the core parsing more robust rather than displaying scores.

The principle behind both is the same: surfacing uncertainty is useful only when the user can do something with the information. Otherwise it erodes trust without providing any value.

---

**shortTitle:** How do you show AI uncertainty in a UI?
**emotion:** thinking
**suggestions:**
- How do you handle unexpected AI output?
- Where does UI add value on top of AI?
- What do you ask before building an AI UI?
- What AI/ML experience do you have?
- What is Folio?
- Tell me about WhatNow

**variants:**
- How do you display AI confidence scores without confusing users?
- How do you show uncertainty in AI output without losing user trust?
- How do you handle showing AI confidence levels in an interface?
