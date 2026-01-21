# Folio

A minimalist portfolio website featuring an AI chatbot assistant that answers questions about skills, experience, and projects using RAG (Retrieval Augmented Generation).

## Overview

Folio is a portfolio website with a single, focused interaction: an AI chatbot that can answer questions about skills, experience, and projects. The name "Folio" references both portfolio and evokes growth (foliage), representing a living, evolving portfolio.

## Features

- **AI Chatbot**: RAG-powered responses using LangChain and OpenAI
- **Single Message Bubble Interface**: Clean, focused design - no scrolling chat history
- **Animated Avatar**: Folio avatar with facial expressions showing AI state
- **Suggested Questions**: Contextual follow-up suggestions
- **Dark Theme**: Forest green color palette with warm terracotta accents
- **Responsive Design**: Mobile-first, same design across all screen sizes

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **RAG Framework**: LangChain
- **LLM**: OpenAI (gpt-4o-mini)
- **Vector DB**: Pinecone
- **Database**: PostgreSQL (SQLAlchemy)
- **Rate Limiting**: Redis
- **Deployment**: Railway

### Frontend
- **Framework**: React + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Architecture**: Event-driven, modular component system
- **Deployment**: Vercel/Netlify

## Project Structure

```
folio/
├── backend/          # FastAPI application
├── frontend/         # React + TypeScript application
└── docs/            # Project documentation
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

## Design

- **Color Palette**: Dark forest green background with soft off-white UI elements and warm terracotta accents
- **Typography**: Plus Jakarta Sans (primary), JetBrains Mono (code)
- **Layout**: Centered, max-width 600px container

## License

[To be determined]

## Author

James Dawson

