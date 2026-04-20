# Integrations Dashboard: Designing for Backend Developers and Sales Simultaneously

The Integrations Dashboard was a specific design challenge: one tool, two completely different audiences. Backend developers worked with data normalisation code. The sales team needed to access and operate on that same data without seeing or understanding the underlying system. The challenge wasn't the data — it was communicating the context around it intuitively for both.

The first move was hierarchy. The dashboard dealt with clients (large real estate companies), branches (individual offices within those companies), and sessions (millions of granular records per branch). Layering these as nested screens made it immediately clear what was a subset of what. Without that structure it was just overwhelming flat data — which is exactly what the original engineer-built version felt like.

Simplification mattered as much as organisation. Traffic-light colours for statuses meant a failed processing job showed as red and was instantly visible without reading anything. All the raw data was still accessible by drilling down, but the default view showed only what a user actually needed at a glance. The backend team got what they needed by drilling into detail; the sales team got what they needed from the top level without ever touching the raw data.

I validated by releasing early, talking to both teams, and shipping frequently based on what they asked for. The original structure was designed to grow — adding new pages and controls was straightforward because the foundation anticipated it. Building in flexibility from the start is what makes iterative validation work without constant rework.

This project taught me that good design for mixed audiences means designing the information hierarchy before the visual design. Who needs what at a glance? Who needs to drill down? What context is essential vs optional? Getting those answers right first makes everything else follow naturally.
