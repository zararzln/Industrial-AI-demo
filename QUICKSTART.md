# Quick Start Guide - Get Running in 10 Minutes

This is the fastest way to get the Industrial AI Platform running.

## Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key

## 5-Step Setup

### 1. Backend Setup (3 minutes)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key (1 minute)

```bash
cp .env.example .env
```

Edit `.env` and add:
```
OPENAI_API_KEY=sk-your-key-here
```

### 3. Initialize Data (2 minutes)

```bash
python scripts/seed_data.py
```

Wait for "Document seeding completed successfully!"

### 4. Start Backend (30 seconds)

```bash
uvicorn app.main:app --reload --port 8000
```

Keep this terminal open. Backend running at http://localhost:8000

### 5. Start Frontend (3 minutes)

Open a NEW terminal:

```bash
cd frontend
npm install
npm start
```

Frontend opens automatically at http://localhost:3000

## Quick Test

1. Open http://localhost:3000
2. Click "Operator View"
3. Select "Hydraulic Pump 7"
4. Ask AI: "What's causing the high vibration?"

You should get a response with recommendations!

## Troubleshooting

**Can't install packages?**
- Backend: Make sure Python 3.11+ is installed
- Frontend: Make sure Node.js 18+ is installed

**OpenAI errors?**
- Check your API key in `.env`
- Verify you have credits: https://platform.openai.com/account/usage

**Port already in use?**
- Backend: Change port in command: `--port 8001`
- Frontend: Change port in `vite.config.ts`

## What's Next?

- Read [README.md](./README.md) for full overview
- Check [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed setup
- See [DEMO_SCRIPT.md](./DEMO_SCRIPT.md) for demo ideas
- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for technical details

## Project Structure

```
industrial-ai-demo/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── agents/      # Multi-agent system
│   │   ├── api/         # REST endpoints
│   │   ├── rag/         # RAG pipeline
│   │   └── services/    # Business logic
│   └── scripts/         # Data seeding
├── frontend/             # React frontend
│   └── src/
│       ├── views/       # Dashboard components
│       └── services/    # API client
└── README.md            # Full documentation
```

## Key Features

✅ **Multi-Agent AI System** - Orchestrated agents for complex queries
✅ **RAG Pipeline** - Searches industrial documentation
✅ **Dual Interfaces** - Executive and Operator dashboards
✅ **Real-time Monitoring** - Equipment health and alerts
✅ **Predictive Analytics** - ML-based failure prediction

## Support

Questions? Issues? Check:
1. API docs: http://localhost:8000/docs
2. Browser console for errors
3. Terminal logs for backend errors

---

**Total Setup Time**: ~10 minutes
**Project Status**: Ready for demo/development
**Author**: Zara Razlan
