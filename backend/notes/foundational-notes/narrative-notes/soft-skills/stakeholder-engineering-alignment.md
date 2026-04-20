# Keeping Stakeholders and Engineers Aligned: The Nexus Feedback Loop

## The Gap That Needs Closing

The most common failure mode between stakeholders and engineers is a gap that nobody is actively closing. Stakeholders have domain knowledge — they know what would make their work more effective — but they can't always translate that into engineering terms. Engineers understand what's technically feasible but don't always understand what's actually valuable to the people using the product. Without someone actively bridging those two, the product is shaped more by what's easy to build than by what's useful, and stakeholders feel unheard.

On Nexus I drove that bridging consistently rather than waiting for it to exist as a formal process.

## The Nexus Feedback Loop

The sales team at Nurtur who would eventually use Nexus had good ideas. They were working with the product from a completely different angle — practical daily use — and they spotted gaps and needs that wouldn't have occurred to someone building from the engineering side. But they had no frontend experience and limited backend understanding, so their suggestions sometimes described solutions rather than problems, or assumed feasibility without knowing the effort involved.

Rather than treating their ideas as requirements to accept or reject, I ran a consistent loop. After each round of suggestions, I'd investigate: mapping what would be needed on the frontend, checking with Craig (my backend developer) on what his side would require. Then I'd come back with a clear picture: what was feasible, what wasn't, and what alternatives might deliver similar value. I asked which trade-offs mattered most to them.

The concrete example that stuck: the sales team suggested regex filtering for a series of entries. It sounded simple but involved significant work on both frontend and backend sides — infrastructure that didn't exist, edge cases to handle, API calls to redesign. Rather than refusing in the meeting, I said I'd investigate and get back to them. I came back with the full picture: here's what it would take, here are alternatives, which matters more to you?

## What the Loop Produced

That process produced better suggestions each time. Stakeholders built a working mental model of what was hard versus easy, what had alternatives versus what was genuinely one-of-a-kind. By the end, requests arrived better-grounded — they knew to flag when something mattered a lot (even if it seemed complex) and to deprioritise nice-to-haves they could see were expensive.

It also meant I learned what was actually valuable, which changed how I thought about what to build next. Engineering priorities align better when you understand which user problems are genuinely painful rather than just interesting.

## Driving It vs Being Given It

This loop wasn't a process handed to me. There was no formal stakeholder liaison role, no scheduled alignment meetings, no requirement to run this cycle. I saw the gap, saw that it cost the project quality, and built the habit of closing it. That's the important part: proactively connecting stakeholders and engineering, pulling usefulness and priorities out of their domain knowledge, aligning that with frontend and backend reality, and feeding clear trade-offs back so the next round of ideas was better-grounded.

Projects like Nexus run on that rhythm constantly because someone has to keep closing the loop.
