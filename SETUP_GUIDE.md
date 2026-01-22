# Setup Guide - Industrial AI Demo

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.11 or higher
- Node.js 18 or higher
- Git
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/industrial-ai-demo.git
cd industrial-ai-demo
```

## Step 2: Backend Setup

### 2.1 Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.3 Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# On Windows, use: notepad .env
# On Mac/Linux, use: nano .env or vim .env
```

Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 2.4 Seed the Database

This will populate the vector store with industrial documentation:

```bash
python scripts/seed_data.py
```

You should see output like:
```
INFO - Initializing RAG pipeline...
INFO - Adding 5 documents to vector store...
INFO - Added 47 chunks from 5 documents
INFO - Document seeding completed successfully!
```

### 2.5 Start the Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at:
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs

Keep this terminal window open.

## Step 3: Frontend Setup

Open a NEW terminal window.

### 3.1 Navigate to Frontend Directory

```bash
cd frontend
```

### 3.2 Install Dependencies

```bash
npm install
```

This will take a few minutes to download and install all packages.

### 3.3 Start the Development Server

```bash
npm start
```

The frontend will be available at:
- App: http://localhost:3000

Your browser should automatically open to the application.

## Step 4: Verify Installation

### Test Backend

In your browser, visit:
- http://localhost:8000/docs

You should see the FastAPI interactive documentation (Swagger UI).

Try the following:
1. Expand the `GET /api/v1/equipment/` endpoint
2. Click "Try it out"
3. Click "Execute"
4. You should see a list of equipment

### Test Frontend

Visit http://localhost:3000

You should see:
1. **Executive View**: Dashboard with KPIs, equipment status, and predicted failures
2. **Operator View**: Equipment list, alerts, and AI assistant

### Test AI Assistant

1. Switch to the **Operator View**
2. Click on any equipment (e.g., "Hydraulic Pump 7")
3. In the AI Assistant section, try asking:
   - "What's causing the high vibration?"
   - "Show me the maintenance history"
   - "What are the recommended actions?"

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'app'`
**Solution**: Make sure you're in the `backend` directory and your virtual environment is activated.

**Problem**: `OpenAI API key not found`
**Solution**: Verify your `.env` file exists and contains `OPENAI_API_KEY=your-key-here`

**Problem**: ChromaDB errors
**Solution**: Delete the `data/chroma` directory and run `python scripts/seed_data.py` again.

### Frontend Issues

**Problem**: `npm: command not found`
**Solution**: Install Node.js from https://nodejs.org/

**Problem**: Port 3000 already in use
**Solution**: Change the port in `vite.config.ts`:
```typescript
server: {
  port: 3001,  // Changed from 3000
  ...
}
```

**Problem**: Can't connect to backend
**Solution**: Ensure the backend is running on port 8000 and check the proxy configuration in `vite.config.ts`.

## Development Tips

### Hot Reload

Both backend and frontend support hot reload:
- Backend: Changes to Python files will automatically restart the server
- Frontend: Changes to React files will automatically update in the browser

### API Documentation

The backend provides interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests

Backend tests:
```bash
cd backend
pytest tests/ -v
```

### Code Formatting

Format backend code:
```bash
cd backend
black app/
```

## Next Steps

1. **Explore the Code**: Start with `backend/app/main.py` and `frontend/src/App.tsx`
2. **Add New Equipment**: Modify `backend/app/services/data_service.py`
3. **Add New Agents**: Extend `backend/app/agents/orchestrator.py`
4. **Customize UI**: Edit components in `frontend/src/views/`
5. **Add Documentation**: Add new documents in `backend/scripts/seed_data.py`

## Docker Setup (Optional)

If you prefer using Docker:

```bash
# Make sure you have Docker and Docker Compose installed
docker-compose up --build
```

This will start all services:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- ChromaDB: http://localhost:8001

## Production Deployment

For production deployment, consider:
1. Use environment variables for all sensitive data
2. Enable HTTPS/TLS
3. Set up proper database (PostgreSQL recommended)
4. Use production-grade vector store (Pinecone, Weaviate)
5. Implement authentication and authorization
6. Set up monitoring and logging
7. Configure auto-scaling for Kubernetes deployment

## Getting Help

If you encounter issues:
1. Check the logs in the terminal
2. Verify all dependencies are installed
3. Ensure your OpenAI API key is valid and has credits
4. Review the troubleshooting section above

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
