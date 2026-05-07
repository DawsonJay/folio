# Factual notes — overview

This folder holds **reference markdown** distilled from portfolios, timelines, and other sources. It is the authoring layer for Tier 1 direct answers — not embedded as RAG corpus by default.

## Purpose

- Single place for **verifiable facts** (dates, stack, visas, timelines)
- Structured by topic file; gaps marked where something still needs confirmation
- **Authoritative inventory = filenames in this directory** — do not rely on enumerated lists elsewhere drifting over time

## How to use

1. Edit the relevant factual file when your career or immigration facts change.
2. Regenerate or update matching Tier 1 notes under `notes/tier-1-direct-answers/`.
3. Re-run `python scripts/embed_direct_answers.py` from `backend/` when Tier 1 text changes.

## Related docs

- [ATOMIC-NOTES-GUIDE.md](../../../docs/ATOMIC-NOTES-GUIDE.md) — writing style for embedding-friendly notes  
- [TIERED-NOTES-SYSTEM.md](../../../docs/TIERED-NOTES-SYSTEM.md) — Tier 1 vs Tier 2 behavior  
