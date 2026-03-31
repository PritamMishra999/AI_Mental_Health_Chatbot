# Mental Health Chatbot

A Python + React web app for AI-powered emotional support, stress detection, and wellness recommendations.

## Features
- FastAPI backend with `/auth` and `/chat` endpoints
- React/Vite frontend chat interface
- External LLM support via OpenAI
- Stress/emotion estimation and personalized recommendations
- User registration and login support

## Setup

1. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

2. Update `.env` with your OpenAI API key and an app secret.

3. Install backend dependencies:

   ```bash
   cd backend
   python -m pip install -r requirements.txt
   ```

4. Install frontend dependencies:

   ```bash
   cd ../frontend
   npm install
   ```

## Run locally

### Terminal 1: Start the backend

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend will run on `http://localhost:8000`

### Terminal 2: Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Then open: `http://localhost:5174`

## Notes
- The backend uses SQLite by default (created in `backend/backend.db`).
- Set `OPENAI_API_KEY` in `.env` before sending chat messages.
- The app is built to support deployment in universities, EdTech, healthcare, and corporate wellness workflows.
- Use two separate terminals: one for backend (port 8000), one for frontend (port 5173).
