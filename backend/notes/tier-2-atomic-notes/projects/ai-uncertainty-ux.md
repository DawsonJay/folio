# AI Uncertainty in UI: When to Surface It and When Not To

Whether to show AI uncertainty to users is not a single answer — it depends on what the AI is for and what the user's relationship with it should be.

On WhatNow the model produces activity recommendations and users train it over time through pairwise choices — picking which of two options fits them better. A low confidence score there isn't a failure state; it's feedback that the next set of choices will help. I reframed uncertainty as the user and AI being on the same side, improving together. Surfacing uncertainty openly made sense because the user had agency over it — low confidence meant more useful training signal, not a broken feature.

Folio is the opposite context. It's a professional showcase and its job is to communicate competence to employers. I only surface uncertainty when confidence falls below the threshold for reliable matching — at that point it returns a clear message that there isn't enough material and suggests alternative questions. Outside that threshold I make the core mechanics more robust rather than displaying confidence scores. Foregrounding uncertainty in a portfolio tool would erode the trust I'm trying to build.

The principle behind both decisions: surface uncertainty only when the user can do something useful with the information. Showing low confidence when there's nothing the user can do just erodes trust without providing value. The question isn't "how accurate is this?" but "what can the user do differently if they know this?"

In CV interfaces the same principle applies. When an item can't be identified, the useful response is concrete recovery options — suggest better lighting, a simpler background, a clearer angle — not just a confidence number. Recovery paths are more useful than scores.

Folio's fallback architecture uses this principle systemically: scripted answers for strong matches (no uncertainty visible), RAG from vetted notes for partial matches (low visibility), and a clear "not enough material" message at the threshold. Each layer handles a different confidence band with appropriate UX.
