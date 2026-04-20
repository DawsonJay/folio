# Jam Hot: Computer Vision, Fruit Classification, and the Real-World Gap

Jam Hot was a computer vision project I built for fruit classification. I trained a model to identify fruit in images using a labelled dataset and achieved 86% validation accuracy. Then I pointed it at real photos — images outside the training set — and real-world accuracy dropped to 0%.

That gap is the central lesson. The model was overfitted to its training data in ways that didn't transfer to real use. 86% in testing meant nothing in practice.

This experience directly shapes how I think about AI UI design. If you design an interface against only the validation story, you build something that confidently shows "detected: apple, 91% confidence" when the model is actually failing on real images. That's actively harmful — worse than an interface that acknowledges the limitation honestly. Users adjust their behaviour based on what the interface tells them. False confidence leads to false reliance.

The question I'd now ask before designing any AI interface: what is the real-world performance, not just the validation accuracy? Those are different numbers and the gap between them determines how honest the interface needs to be. If the real-world performance is significantly lower, the UI needs to communicate that — perhaps through lower confidence thresholds for displaying results, honest fallback states, or prompts that help users get better inputs (better lighting, simpler backgrounds).

Computer vision more broadly: it's the use of AI to identify subjects of relevance in images — objects, faces, or more abstract scene understanding. It's historically hard for computers; humans have always outperformed software at visual understanding. The value once achieved is scale: processing large amounts of visual data faster than any human team could. Applications include law enforcement (reviewing large quantities of surveillance data) and military use (targeting systems that function despite jamming).

My CV expertise is honest: I understand the fundamentals and have first-hand experience with the validation-vs-reality problem. My frontend skills are directly applicable to CV products. Technical depth on the CV side I'd build through immersion — the same way I built backend knowledge at Nurtur.
