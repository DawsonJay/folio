# How do you handle production bugs?

For bugs in projects I owned, I tried to catch them early — and when I did, my focus was on what the bug was telling me about the code structure rather than patching the symptom. Was it cracking under more data? A new feature that didn't fit cleanly? Two competing approaches to the same problem? The Nexus Dashboard had race conditions from multiple asynchronous API calls coming in together. Rather than patch over the specific case, I restructured how those calls were handled to make the whole system more predictable. That prevented the same class of problem appearing again as the project grew.

For user-reported bugs, the problem is usually more calcified by the time it surfaces. I investigate the surrounding code, understand the root cause, and fix it at the deepest level a surgical change will allow.

The trickiest production bug I dealt with was one where properties transferred between lists would silently reappear in the original list hours or a day later. It crossed frontend, backend, queues, and orchestrators. I used dummy data and manually traced a transfer through the system, adjusted cron timers to avoid waiting hours between cycles, and eventually found that under a very specific set of conditions an object was being remade from scratch — and a single ID field was left out. Without that ID, the system moved it back by default. One field missing in one code path, only triggered by a rare intersection of processes. One line to fix it.

---

**emotion:** thinking
**suggestions:**
- Tell me about debugging a complex issue
- What's your debugging process?
- How do you approach problem-solving?
- What's your strongest React skill?
- How do you approach technical debt?
- Tell me about a challenging project

**variants:**
- How do you handle bugs in production?
- What do you do when a bug is reported in production?
- Walk me through how you debug a production issue
