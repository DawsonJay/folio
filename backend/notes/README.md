# Notes for the Folio RAG system

Markdown under `backend/notes/` powers the assistant: **Tier 1** hand-written recruiter Q&A (high-precision, low/no LLM) and **Tier 2** semantic chunks for full RAG. Foundational factual/narrative material also lives here for authoring and consistency.

## Layout (current)

| Area | Role |
| ---- | ---- |
| `tier-1-direct-answers/` | Polished answers; one `# Title` question per file. `metadata/` holds catalogs — excluded from embeddings. |
| `tier-2-atomic-notes/` | Atomic corpus (+ project/topic markdown) used by Tier 2 retrieval. |
| `foundational-notes/` | Authoring references (factual + narrative summaries). |
| Other legacy category trees | May appear under `notes/`; **`embed_notes.py`** embeds almost all `.md` under `notes/` (see script exclusions). |

Exact file counts drift over time — the folders above are the source of truth, not counts in stale README bullets.

## Embeddings

From `backend/`:

```bash
python scripts/embed_direct_answers.py   # Tier 1 only → embeddings.json metadata type direct_answer
python scripts/embed_notes.py            # Tier 2 + breadth (excludes paths named `metadata` and template filenames)
```

Details: **`backend/docs/SETUP-INSTRUCTIONS.md`**, **`backend/docs/TIERED-NOTES-SYSTEM.md`**.

## Writing guidelines

- Tier 2 style guide: **`backend/docs/ATOMIC-NOTES-GUIDE.md`**  
- Direct-answer specs/templates: **`tier-1-direct-answers/metadata/`**
