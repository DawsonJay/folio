# Jam Hot: Computer Vision Project and the Validation vs Real-World Gap

Jam Hot was a computer vision project I built for fruit classification. I trained a model to identify fruit in images and achieved 86% validation accuracy — a number that looked solid in testing. Then I pointed it at real photos rather than the training set and real-world accuracy dropped to 0%.

That gap between validation performance and real-world performance is the most important thing I took from the project. The model was overfitted to its training data in ways that didn't transfer to actual use. This experience directly shaped how I think about AI UI design: if you build an interface against only the validation story, you build something that confidently displays "detected: apple, 91% confidence" when the model is actually unreliable on real images. That's worse than an interface that acknowledges the limitation honestly.

The lesson I'd apply to any AI UI project: always ask about real-world vs validation performance before designing. Those are two different numbers and the gap between them determines how honest the interface needs to be. A UI that shows high-confidence results for a poorly-performing model actively misleads users.

Jam Hot is also the starting point for my understanding of computer vision. I know CV is the use of AI to identify subjects of relevance in images — discrete objects, faces, or more abstract scene understanding like how multiple elements are interacting. I understand the validation vs real-world performance gap from direct experience. My frontend skills are immediately applicable to CV product work; the CV-specific depth I would build through immersion, the same way I built backend knowledge by joining the Integrations team at Nurtur.

The failure of Jam Hot wasn't about giving up on AI — it was learning the right scope and the right questions to ask before building. WhatNow, moh-ami, and Folio all came after and all succeeded. The Jam Hot lesson about real-world performance shaped the design of each of them.
