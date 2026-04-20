# Building a UI for AI Detection Results: Bounding Boxes, Confidence, and Edge Cases

If I were building a UI that displays object detection output — bounding boxes, confidence scores, object classes — the first question is who it's for and what they need to do with the information.

If the goal is making the model's reasoning legible, I'd structure it as: source image with bounding boxes overlaid on one side, breakdown of object classes with confidence scores on the other, and the final determination separated out with its own confidence score. The aim is letting the user see the model's logic without being overwhelmed by it.

Before designing anything I'd want to know the real-world performance picture, not just validation numbers. My closest experience is Jam Hot — a CV project that hit 86% validation accuracy then dropped to 0% when pointed at real photos. That gap taught me that if the model's real-world failure modes aren't surfaced honestly in the interface, users have no way to compensate. An interface showing high-confidence results for a poorly-performing model actively misleads users.

For edge cases: multiple overlapping detections get different colours on the source image so the conflict is visible. Low confidence at the final determination stage gets flagged explicitly. Earlier pipeline stages can have low confidence for specific classes without that being an error — a table being classified as furniture rather than fruit is expected, not a failure. Complete misses still need to show the logic steps taken. The worst UX is when something has clearly gone wrong with no explanation of why.

The things I'd want to know from the ML team before designing: real-world vs validation performance gap; what the model commonly gets wrong; what kinds of inputs are difficult; the large abstract steps in the detection logic so the UI can display progress meaningfully; and whether the interface should be a display tool or a debugging tool (drilling down for detail serves different users differently).
