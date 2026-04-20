# AI Vision and UI Design: Computer Vision, Jam Hot, and Uncertainty

## What Computer Vision Actually Is

Computer vision is the use of AI to identify subjects of relevance in an image. That can mean identifying discrete objects — classifying fruit, recognising faces — or more abstract understanding of a scene: what's happening, how multiple elements are interacting, relationships between subjects. It's historically one of the hardest tasks for computers; humans have always outstripped software at visual understanding. The processing power once that capability is achieved is what makes it so valuable at scale — large amounts of footage processed quickly in ways no human team could manage.

Applications span widely. Law enforcement often has huge quantities of surveillance data and not enough people to review it case by case; CV addresses that throughput problem. Military applications include AI in drones that can still identify and hit targets despite jammers disrupting the operator connection. These are the live use cases, not speculative ones.

## Jam Hot: The Real-World Accuracy Problem

Jam Hot was a computer vision project I built for fruit classification. I trained a model to identify fruit in images and achieved 86% validation accuracy — a number that looked solid in testing. Then I pointed it at actual photos rather than the training set and the real-world accuracy dropped to 0%.

That gap — between validation performance and real-world performance — was the most important thing I took from the project. The model was overfitted to its training data in ways that didn't transfer. This has a direct implication for UI design: if you build an interface against only the validation story, you build something that confidently shows "detected: apple, 91% confidence" when the model is actually unreliable on real images. That's worse than an interface that acknowledges the limitation honestly.

The lesson I'd now apply to any AI UI: always ask about real-world vs validation performance before designing. Those are two different things, and the UI has to be honest about which it's reflecting.

## Building a UI for AI Detection Results

If I were building a UI that displays object detection output — bounding boxes, confidence scores, object classes — the first question is who it's for and what they need to do with the information.

If the goal is making the model's reasoning legible, I'd structure it as: source image with bounding boxes overlaid on one side, breakdown of object classes with confidence scores on the other, and the final determination separated out with its own confidence score. The aim is letting the user see the model's logic without being overwhelmed by it.

For edge cases: multiple overlapping detections get different colours on the source image so the conflict is visible. Low confidence at the final determination stage gets flagged explicitly. Earlier stages of the pipeline can have low confidence for specific classes without that being an error — a table being classified as furniture rather than fruit isn't a mistake. Complete misses still need to show the logic steps the model took. The worst UX is when something has clearly gone wrong but there's no explanation of why.

The thing I'd want to know before designing any of this is the model's real-world failure modes. If I know what it commonly gets wrong, I can structure the UI to communicate those patterns rather than hiding them.

## AI Uncertainty in UI: When to Surface It

The question of when to show AI uncertainty to users is not a single answer — it depends on what the AI is for and what the user's relationship with it should be.

On WhatNow the model produces activity recommendations and the user trains it over time through pairwise choices — picking which of two options fits them better. A low confidence score there isn't a failure, it's feedback that the next set of choices will help. I reframed uncertainty as the user and AI being on the same side, improving together. Surfacing uncertainty openly made sense because the user had agency over it.

Folio is the opposite context. It's a professional showcase and its job is to communicate competence. I only surface uncertainty when confidence falls below the threshold for reliable matching — at that point it returns a clear message that there isn't enough material and suggests alternative questions. Outside that threshold I make the core mechanics more robust rather than displaying uncertainty scores.

The principle behind both: surface uncertainty only when the user can do something useful with the information. Showing low confidence when there's nothing the user can do just erodes trust without providing value.

## Folio's Three-Layer Fallback

The most defensive AI UI design I've built is Folio's fallback architecture. As an open chat interface that's also a professional showcase, it has to handle any question without confidently serving wrong information.

The design is three layers. First: scripted answers for common questions, bypassing the LLM entirely — cheaper, faster, more testable. Second: if no scripted answer matches, RAG retrieves the closest atomic notes and the LLM composes from vetted material, reducing hallucination. Third: if nothing matches well enough, a clear message that there isn't enough material, with suggestion chips pointing to better-covered territory.

The layered approach means Folio degrades gracefully rather than failing noisily. A gap in coverage produces an honest message and recovery options, not a confident wrong answer.
