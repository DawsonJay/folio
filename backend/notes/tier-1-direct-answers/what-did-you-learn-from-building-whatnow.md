# What did you learn from building WhatNow?

The most important lesson: for individual developers, data acquisition is typically the insurmountable barrier to completing AI projects. Academic ML focuses on algorithms and benchmarks, assuming datasets exist. Real-world ML requires solving how to get quality data. WhatNow works because it generates its own data through usage. This insight now guides my project selection - I look for AI applications where the data problem is solvable.

I learned to start simple and add complexity when needed. WhatNow started as vanilla JavaScript and basic linear contextual bandits. It evolved to React, TypeScript, Redux, semantic embeddings, and two-layer learning as needs became clear. Starting with full complexity upfront would have been overwhelming. Starting simple and adding sophistication incrementally made the project achievable and kept it functional at every stage.

Production is different than development. Deployment constraints shaped major technical decisions - lightweight custom implementations instead of heavy ML libraries, client-side Session AI for zero-latency learning, careful database migration procedures, comprehensive error handling. Production systems need to handle unreliable networks, platform constraints, real user behavior, and ongoing maintenance.

I learned pragmatic ML engineering choices. Using sentence transformers over LLMs for semantic matching because they're faster, cheaper, and more reliable. Implementing two-layer learning (Session AI + Base AI) to balance responsiveness with stability. Choosing to pivot from manual metadata to AI embeddings when the approach wasn't scaling. These decisions prioritize what works over what's theoretically elegant.

WhatNow taught me that building complete systems end-to-end provides more learning than perfect prototypes. The project is fully deployed, genuinely useful, and continues to improve through real usage.

---

**emotion:** thinking
**suggestions:**
- Tell me about WhatNow
- How did you come up with the WhatNow idea?
- What was hardest about building WhatNow?
- How do you approach learning new tech?
- What future projects are you considering?
- How do you approach AI project scoping?

**projectLinks:**
- WhatNow:
  - demo: https://whatnow.onrender.com/
  - github: https://github.com/yourusername/whatnow
