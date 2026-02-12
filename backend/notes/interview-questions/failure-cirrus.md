## Question

Tell me about a time you failed, or a project that didn't go as planned.

## Answer

A meaningful failure for me was a personal project called Cirrus, where I set out to build an AI‑driven system to predict wildfires on a map across Canada. The idea was to use free historical weather data from NOAA, but I ran into a fundamental data problem I couldn't solve.

The data came from weather stations scattered inconsistently across Canada—some areas like the tundra had zero coverage, and in remote regions stations were sometimes tens of kilometres apart or more. I tried to interpolate the data onto a grid to fill the gaps, but that meant some tiles were essentially guesses that weren't reliable enough for something that might influence real wildfire‑risk decisions. At that point I had to accept the project wasn't going to work and stop rather than putting out something people couldn't trust.

I took two big lessons from that. First, I need to validate my assumptions about data quality and coverage early, not after I've built half the system. Second, I need clear criteria for when to stop so I'm not just following sunk costs forward. Those lessons directly influenced how I approached later projects like the self‑teaching recommendation system and my portfolio chatbot: I now prototype on small, representative data, measure whether it's actually good enough for the use case, and only scale once I know the foundations are solid. That's the kind of early validation I'd encourage on any team project—making sure the data constraints are clear before we commit resources.

## Concepts to memorise

1. The failure  
   - Personal project: Cirrus, an AI‑driven wildfire prediction system for Canada that failed.  
   - Idea: use free historical NOAA weather data to visualise wildfire risk.  
   - Ran into a fundamental data problem I couldn't solve.

2. The fundamental data problem  
   - Weather stations scattered inconsistently across Canada; some areas (e.g., tundra) had zero coverage.  
   - In remote regions, stations were sometimes tens of kilometres apart or more.  
   - Tried to interpolate data onto a grid to fill gaps.  
   - Result: some tiles were unreliable guesses—not good enough for wildfire‑risk decisions.

3. The decision  
   - Had to accept the data problem was fundamental and the project wasn't going to work.  
   - Chose to stop rather than putting out something people couldn't trust.

4. Lessons and changes  
   - Validate data quality and coverage early, not after building half the system.  
   - Define clear stop criteria to avoid sunk‑cost thinking.  
   - Apply those lessons to later AI/RAG projects: prototype on small representative data, measure quality against the use case, only scale once foundations are solid.  
   - That's the kind of early validation you'd encourage on any team project—making sure constraints are clear before committing resources.

