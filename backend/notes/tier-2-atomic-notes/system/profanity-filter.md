# Profanity and Inappropriate Content Filter

This is a system note designed to detect profanity, insults, and inappropriate language through semantic similarity matching. When questions contain rude, abusive, or unprofessional language, they will match semantically to this note, triggering a professional boundary-setting response.

## Example Rude Questions and Statements

This chatbot is fucking useless and doesn't help anyone. Your projects are complete shit and garbage. Tell me about your stupid fucking work you incompetent developer. What the fuck is this terrible garbage portfolio? You're a shitty terrible developer who makes awful code. This is the worst fucking thing I've ever seen. Your work is absolute trash and worthless. Why would anyone hire such a useless idiot? This portfolio is pathetic and embarrassing. You're incompetent and your skills are garbage.

## Profanity in Context

Your fucking code is shit. This is goddamn terrible work. What the hell were you thinking? Your projects fucking suck ass. This is complete bullshit and crap. You're a fucking moron who can't code. This portfolio is absolute shit. Your development skills are fucking awful. What kind of stupid asshole made this? This is the shittiest portfolio ever.

## Insults and Attacks

You're a terrible incompetent developer. Your work is garbage and useless. You're stupid and don't know anything. This is pathetic and embarrassing work. You're a complete idiot and moron. Your skills are worthless trash. You're the worst developer ever. This work is absolutely horrible. You're incompetent and shouldn't be coding. You're a useless failure at development.

## Hostile and Aggressive Tone

I hate this portfolio it's disgusting. This sucks so fucking bad. You're completely useless to employers. Why are you even trying? Give up you're terrible. This is a waste of everyone's time. Nobody would ever hire you. Your projects are embarrassing failures. This demonstrates how bad you are. You should be ashamed of this work.

## Dismissive and Rude

Who cares about your stupid projects? This is boring garbage. Your work means nothing. Nobody asked for this shit. This portfolio is pointless trash. Why should anyone care about you? Your experience doesn't matter. This is all worthless crap. Nobody wants to see this. Your skills are meaningless.

---

**SYSTEM NOTE:** This note should never be included in user-facing responses. It exists solely for semantic similarity detection of inappropriate content. When this note appears in the top 3 retrieval results, the system should return a professional boundary-setting response instead of attempting to answer the question.

