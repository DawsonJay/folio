# How did you handle difficult situations at work?

The Nexus Dashboard performance problem is a good example. Dashboard load time was 15+ seconds, which made it nearly unusable. This wasn't a single bug to fix - it was a fundamental architectural issue requiring systematic investigation and solution.

I approached it by understanding the root cause first, not just treating symptoms. I investigated what was actually loading, identified that we were fetching full objects when we only needed counts, and analyzed which data was used immediately versus later. The solution involved strategic loading (counts first, full objects on demand), buffer systems to prevent repeated API calls, React Query caching for data reuse, and displaying progress so users understood what was happening.

Load time dropped from 15+ seconds to sub-5 seconds. This required balancing user experience, backend constraints, and frontend architecture - not just optimizing code but rethinking how data flowed through the system.

Another difficult situation: leaving the Email Editor project mid-development to work on Nexus in October 2025. The team depended on me for frontend architecture and mentoring. I handled the transition by documenting my work thoroughly, ensuring the 3 backend developers I'd been mentoring could continue without me, and making sure no critical tasks were left incomplete. The project continued successfully after I left.

Difficult situations require understanding the real problem (not just symptoms), systematic investigation, pragmatic solutions that balance constraints, and clear communication with stakeholders.

---

**shortTitle:** How do you handle difficult work situations?
**emotion:** thinking
**suggestions:**
- Tell me about debugging a complex issue
- How do you approach problem-solving?
- Tell me about the Nexus Dashboard
- How did you grow in your position at Nurtur?
- Tell me about the Email Editor project
- Tell me about a difficult situation?
