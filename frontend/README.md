# Folio frontend

React + TypeScript + Vite app for [Folio](../README.md): portfolio UI, AI chat UX, EmailJS contact form.

## Prerequisites

- Node.js 18+
- Backend running separately (or via `npm run dev:all`) when testing live chat

## Scripts

| Command | Purpose |
| ------- | ------- |
| `npm install` | Install dependencies |
| `npm run dev` | Vite dev server (`http://localhost:5173`) |
| `npm run dev:backend` | Start FastAPI via `backend/venv` (`scripts/dev-backend.mjs`) |
| `npm run dev:all` | Frontend + backend concurrently |
| `npm run build` | Typecheck + production build (`dist/`) |
| `npm run preview` | Preview production build locally |
| `npm run lint` | ESLint |
| `npm test` | Vitest |
| `npm run test:coverage` | Coverage |

## Routes

Configured in [`src/App.tsx`](src/App.tsx) (typically `/`, `/get-in-touch`, `/get-in-touch/sent`).

## Environment variables

Create **`frontend/.env`**:

```env
VITE_EMAILJS_SERVICE_ID=your_service_id
VITE_EMAILJS_TEMPLATE_ID=your_template_id
VITE_EMAILJS_PUBLIC_KEY=your_public_key
```

Optional:

```env
VITE_API_URL=https://your-api-host.example
```

## Architecture notes

- **Events:** [`src/events/README.md`](src/events/README.md) — typed event bus for chat flow  
- **API:** [`src/api/ChatApiClient.ts`](src/api/ChatApiClient.ts)  

## Backend docs

Setup, embeddings, deployment: **`../backend/docs/`** (see [`backend/docs/README.md`](../backend/docs/README.md)).
