# Direct Answers — Input Questionnaire

Your answers here will be used to write or rewrite 8 direct answer files in `backend/notes/tier-1-direct-answers/`.
Answer however you naturally talk — fragments, rambling, examples, whatever. I'll shape it, not invent it.
Aim for enough that I understand what you actually think, not a polished answer.

---

## 1. How do you approach performance optimization?

*(Rewriting existing file — current version feels generated)*

**a) When something is slow, what's your actual first instinct before you do anything?**

> I investigate to find where the bottlenecks are and if any of them are easy to fix. Sometimes bottlenecks are fundemental, the server is too limited and there's too much data that you have to keep. it's still worth fixing the bottleneck of course, but it's more valuable to look for easier ones first. for example in nexus where things were slow because we were importing a million objects when all the screen displayed was a count of 4 million. Getting a high level view first allows me to better direct my efforts.

**b) Walk me through what happened with the Nexus Dashboard. What did you think was wrong before you started digging? Were you right?**

> It didn't require that much digging. it was the kind of web page where you go off and get tea while it's loading, which is of course unacceptable for speed. So it was clear that the problem was how much data we were fetching. the interesting bit was considering when the user required what data and seperating the pages into sections and layers so the user only fetched the data they needed at that moment.

**c) Is there anything about performance that you find interesting or satisfying — or is it just problem-solving like anything else?**

> I find structure really interesting in software. Performance is just a symptom of a flawed or insufficient structure. I also like thinking into the future. Bottlenecks happen when the structure was never designed for this scenario in mind. either through a lack of foresight or imagination.  Thinking of the code as a whole, a structure that has to deal with a changing enviroment into the future is what really excites me.

---

## 2. Tell me about a technical decision you'd do differently

*(Rewriting existing file — current version may not reflect what you'd actually pick)*

**a) What's the first decision that comes to mind when someone asks you this? (Not the "best" answer — the one you actually think of)**

> I think of the cirrus project. there was so much trouble with the source data that i eventually had to scrap the project. The code was good, the idea was brilliant, it had all the hallmarks of a project I could be really proud of but the source data was patchy and inconsistant and scattered.

**b) What was the real consequence? Did it cost you time, cause a bug, create a headache?**

> I had to dispose of the entire project because it was just unfixable. I couldn't change the data as it came from an outside source and the project was dependant on it.

**c) What would you actually have done instead?**

> What I actually did for whatnow, which was build the project around a data source that i could control. Instead of relying on a database online or going out and collecting thousands of images myself, I made the ai in what now train incrementally using user input. Like using a waterwheel to power the project. In more general terms I now sketch out what it absolutly foundational to the project and investigate it properly. If i had done real data analysis ont he database i used for cirrus i would have avoided the whole thing, and maybe have been able to make a different project with the same data.

---

## 3. Describe your ideal work environment

*(Rewriting existing file — current version is mostly invented)*

**a) What's the best working situation you've actually been in — even partially? What made it work?**

> Oddly, it wasn't really a work enviroment but it was doing group projects at uni. being in a group of 3-4 people where we all had a clear goal and all had our own part in making it happen. I liked coming together to discuss the project but being able to break away into smaller groups or solo to work on one speciifc part. I liked sharing what we'd done with the group and working as a team to make a great project.

**b) What's made work feel genuinely bad, not just meh?**

> being undervalued. My previous job I was given more and more responsibilies but never the title or pay to go with it. But i still had all the work and blame if anythign went wrong. It felt like being used. There was also a lack of trust. I don't like feeling like every move is being analysed for mistakes because why work hard for someone who's ready to stab you in the back the first chance they get?

**c) What does a good working day feel like to you? What needs to be true for it to feel like good work?**

> I need to feel like i'm supporting the team. One of the reasons i loved working on the nexus dashboard so much was because it was an internal project for the sales team. I knew that it would make their work lives so much easier and better and that inspired me to make the best design and product that i could. I also like working with people who share the same mission, who are inspired to do the work in the same way i am.

---

## 4. What kind of problems do you find most interesting?

*(Rewriting existing file — "cleverness over resources" framing is mine, not yours)*

**a) What's a problem that actually made you excited when you understood what it was?**

> I loved thinking about the atlantis project. I find it facinating to work inside of strong constraints with minimal resources. Atlantis was all about finding a way to photo underwater ruins with a raspberry pi and the limitations of water and cost inspired some very creative solutions that I love. I think it stands in contrast to project with unlimited budget and vague specification, you tend to get lazy bloated code and the solution to every problem is to just use more resources.

**b) Is there a type of problem that consistently gets you going? Or is it more about the specific situation?**

> I like to think of projects as a whole, thinking of the structure and architecture of the code. All the code acting together as an ecosystem and it's structure is what keeps it balanced. an example would be nexus, where I structured things in a modular way with layers to allow for the drilling down of information and reusable parts. it allowed new pages to be build rapidly out of existing building blocks and dramatically reduced fralie code and bugs because using shared building blocks meant that all the foundational code was bulletproof. Thinking of the whole project, and the way it will respond and grow is facinating to me.

**c) What's boring? What kind of work drains you?**

> Work that I know doesn't matter and that won't help anyone. It's draining when you know that you could write terrible code and no one would ever notice or care, all that matters is speed. And you know it'll come back to bite the company in a month and they'll blame you, but in the moment they just want rubbish churned out as fast as possible. I don't tend to gold plate things, but I like to make well designed code that will last for years, like i did for the integrations dashboard.

---

## 5. How do you approach technical debt?

*(New file — currently answered by RAG, non-deterministic)*

**a) What's your actual stance on debt — is some of it fine, or do you try to keep it minimal?**

> I think it's like house keeping. if you try to keep everything absolutely immaculate you never get anythign done at all. But obviously there's a difference between a little clutter on a table and broken windows. I tend to structure my code carefully so in a way to assist this. I make it modular so when you do tidy up, it's only a small self contained section thats risk free to fix and I structure it to be stable and long lasting because structure is hard to fix later. everythign else like variable names inside the scope of that module and using for loops instead of maps and so on is clutter that you can clean up easily later. Usually as part of a sweep through a bunch of modules when things are slower and there's not much serious work to do

**b) Have you inherited bad debt? What did you actually do with it?**

> Yes. When I started at briefyourmarket as a junior developer my first job was debugging Build. Build was a big piece of architechture that they hired a bunch of contractors to rapidly build for for them. but being contractators they didn't care about quality or how easy it was to maintain. So every time there was a bug, because everything was so entangled any useful change would have required remaking the whole system, they just did a hotfix on top, and over years these layered and got more entangled until you ended up with a system that was almost organic in it's complexity. and that no one wanted to touch because it was confusing and unstable and touching anything tended to make a cascade of bugs somewhere else, and Build was utterly critial to the company. So my job was to look for the cause of a bug, investigate it deeply and then make a surgical change that would affect nothing else. That experince taught me both a lot about debugging, but also about struturing code correctly and the value of it. The kind of mistakes that calcify over time into something that's impossible to fix. That's why I talk about structure and thinking into the furtur. I make code that is stable by nature, that can't degrade into something like Build

**c) Have you deliberately created debt — shipped something you knew was imperfect? Was it the right call?**

> mmm, this relates back to what i said about clutter vs broken windows. I've shipped imperfect code because it was important to get it out quickly and it wasn't the kind of debt that gets worse over time. But i've never shipped the other kind because I care about the codebase. FOr the same reason I wouldn't leave a broken window in my house. I have to live there.

---

## 6. How do you decide when to refactor versus rewrite?

*(New file — currently gets a "question is a little vague" RAG response)*

**a) Is there a real example where you made this call — either way?**

> Structure is interesting and valuable because it guides the direction of code. The way I wrote Nexus forces future developers to work in the direction i envisioned because it's the easiest way to do so. it's working with the grain. However, this can work against you too if the structure pushes you in the wrong direction. I think refactoring is the right call when it's only bending the structure, but if the structure forces a direction that's too off course then the only option is to rewrite, as anything else is fighting the nature of the code, and you'll end up rewriting the code in the end anyway.

**b) What does the decision actually feel like? Is there a threshold, or is it more instinctual?**

> As i've said before, i tend to keep one eye on the project as a whole, I know the shape of it and when what i'm trying to do is fighting the structure of the system, not just one small part. So it's intuitive in that it feels light fighting against the current, but that instinct is based on real knowledge of hwo the system works and fits together.

**c) Have you ever got it wrong — refactored when you should have rewritten, or vice versa?**

> Not when it was my decision. I've mentioned build and absolutely the right choice there was to build something new from scratch, but that wasn't my call. My intuiting for programming is fairly unneering 

---

## 7. Why do you want to work at a startup rather than a large company?

*(New file — currently answered by RAG)*

**a) Have you ever seriously considered or interviewed at a larger company? What was the pull?**

> Lots of times, but usually because I badly needed a job and I didn't have the time to shop around for the perfect workplace. Large companies hire more easily, though i find them harder to work with.

**b) What specifically about startups works for you — beyond "move fast" and "ownership"?**

> I've mentioned supporting my team to be a major thing for me, thats much more real in a startup. in a larger company there are larger political currents that i can't do anything about. because startups are so small the attidute of the team has real impact, and the efforts i put into making it better show real results. Working in a larger company that tends to get drowned out by poor management and communication. I also like the heightened communication with management. if there's a problem it's much easier to communicate that in a way that someone will listen. there are less silos and ego in a startup

**c) Is there anything you'd miss or trade off going startup? Be honest.**

> Large companies tend to pay better and be more stable. that's nice but not something that drives me. I suppose working for google or nasa or something has prestige associated with the name which is useful in future job applications, but there's nothing big companies have that matter to me half as much as the kind of team i get to work in and the learning opportunities i would be afforded

---

## 8. What are your weaknesses as a developer?

*(Rewrite needed — current answer is a reframe ("artistic intuition") not a real weakness)*

**a) What's a genuine weakness — something that has actually caused a problem or cost you something?**

> I need to know why something matters. I've never been someone who can work blindly on a project and not care what it's being used for or how it adds to the world. I can become disconnected when I don't see the point in what we do.

**b) What have you done about it?**

> I tend to do my own research into the company and work to reframe things so it's something I can get enthused about.

**c) Has it got better? How would you know?**

> Well it's gotten better in the way that I look for companies that contribute something to the world that I can support. The overarching purpose of my last company was sending out junk mail for estate agents, and while i could get excited about making internal code to help my team members, I was never going to be inspired by the company as a whole

---

*Once you've filled this in, hand it back and I'll write all 8 files.*
