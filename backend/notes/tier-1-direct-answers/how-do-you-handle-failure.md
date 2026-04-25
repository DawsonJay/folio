# How do you handle failure?

Failure is information. The question isn't whether things will go wrong — they will — it's whether the same thing goes wrong twice.

When something fails I fix it in a way that addresses the cause, not just the symptom. The Integrations Dashboard's record of zero maintenance isn't because nothing went wrong during development — it's because when things did go wrong, I fixed them in ways that prevented the same failure from happening again. That distinction between fixing and patching is something I try to be deliberate about.

On the design side, my approach is to get feedback early so failures stay small. On both the Integrations and Nexus dashboards, I took designs to the teams who'd actually use them before committing to a direction. Early feedback means lots of small, cheap failures rather than one large, expensive one late in the process when everything is harder to change. Jam Hot is the counter-example: I built a computer vision model on a dataset that looked good in validation (86% accuracy) before testing it in real conditions, where accuracy dropped to 0%. The lesson from that project shaped everything I've built since — I test assumptions against reality as early as possible.

---

**emotion:** thinking
**suggestions:**
- Tell me about a project that failed
- Tell me about a mistake you made
- How do you approach problem-solving?
- Describe your ideal work environment
- Tell me about the Integrations Dashboard
- Tell me about the Nexus Dashboard
