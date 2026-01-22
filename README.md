# 🏭 Industrial AI Analytics Platform

A production-ready GenAI platform for industrial operations, featuring multi-agent workflows, RAG pipelines, and real-time equipment monitoring.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/react-18.0+-blue.svg)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Project Overview

This platform demonstrates end-to-end AI-powered industrial analytics, combining:
- **Multi-agent orchestration** using LangGraph for complex industrial queries
- **RAG pipeline** for equipment documentation and maintenance history
- **Real-time monitoring** of industrial equipment metrics
- **Dual interfaces** for executives (strategic) and operators (tactical)

**Built for**: Demonstrating production-grade AI engineering capabilities for industrial use cases

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                           │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  Executive View  │         │  Operator View   │          │
│  │  - KPI Dashboard │         │  - Equipment Mon.│          │
│  │  - Insights      │         │  - Maintenance   │          │
│  └──────────────────┘         └──────────────────┘          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Multi-Agent Orchestrator (LangGraph)       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌─────────────────┐   │   │
│  │  │ Analysis │  │ Retrieval│  │  Recommendation │   │   │
│  │  │  Agent   │  │  Agent   │  │     Agent       │   │   │
│  │  └──────────┘  └──────────┘  └─────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │   RAG Pipeline   │         │  Time Series DB  │          │
│  │  - ChromaDB      │         │  - Equipment Data│          │
│  │  - Embeddings    │         │  - Sensor Data   │          │
│  └──────────────────┘         └──────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Key Features

### 1. Multi-Agent System
- **Analysis Agent**: Processes equipment metrics and identifies anomalies
- **Retrieval Agent**: Searches maintenance documentation using RAG
- **Recommendation Agent**: Provides actionable insights based on context

### 2. RAG Pipeline
- Semantic search over equipment manuals and maintenance logs
- Context-aware responses using ChromaDB vector store
- Automatic document chunking and embedding generation

### 3. Dual Interface Design
- **Executive Dashboard**: High-level KPIs, cost analysis, predictive insights
- **Operator View**: Real-time equipment status, maintenance alerts, detailed metrics

### 4. Industrial Data Simulation
- Realistic time-series sensor data (temperature, pressure, vibration)
- Equipment lifecycle events and maintenance history
- Anomaly injection for testing alert systems

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional, for ChromaDB)

### Backend Setup

```bash
# Clone repository
git clone https://github.com/yourusername/industrial-ai-demo.git
cd industrial-ai-demo

# Setup Python environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Initialize database and seed data
python scripts/seed_data.py

# Run backend server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will be available at `http://localhost:3000`

## 📊 Demo Usage

### 1. Executive View
- View overall equipment health score
- Monitor cost metrics and efficiency trends
- Review AI-generated strategic recommendations

### 2. Operator View
- Real-time equipment monitoring
- Maintenance task management
- Query equipment documentation with natural language

### 3. AI Assistant
Try these example queries:
- "What's causing the temperature spike in Compressor-001?"
- "Show me the maintenance history for Turbine-003"
- "What are the recommended actions for the high vibration alert?"

## 🛠️ Technical Stack

### Backend
- **FastAPI**: High-performance API framework
- **LangGraph**: Multi-agent workflow orchestration
- **ChromaDB**: Vector database for embeddings
- **OpenAI GPT-4**: Language model for agents
- **Pydantic**: Data validation and serialization

### Frontend
- **React 18**: Component-based UI framework
- **TypeScript**: Type-safe JavaScript
- **Recharts**: Data visualization
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client

### DevOps
- **Docker**: Containerization
- **pytest**: Testing framework
- **GitHub Actions**: CI/CD (configured)

## 📁 Project Structure

```
industrial-ai-demo/
├── backend/
│   ├── app/
│   │   ├── agents/           # Multi-agent implementation
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Configuration and utilities
│   │   ├── models/           # Data models
│   │   ├── rag/              # RAG pipeline implementation
│   │   └── services/         # Business logic
│   ├── data/                 # Sample industrial data
│   ├── tests/                # Test suite
│   ├── scripts/              # Utility scripts
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── views/            # Executive & Operator views
│   │   ├── services/         # API integration
│   │   └── utils/            # Helper functions
│   ├── public/
│   └── package.json
├── docker-compose.yml
├── .github/workflows/        # CI/CD configuration
└── README.md
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test
```

## 🎯 Key Design Decisions

### 1. Multi-Agent Architecture
Used LangGraph for transparent agent orchestration with clear state management, enabling complex reasoning chains while maintaining debuggability.

### 2. RAG Implementation
Chose ChromaDB for its simplicity and performance in development, with straightforward migration path to production vector databases like Pinecone or Weaviate.

### 3. Data Model
Designed around real industrial scenarios (predictive maintenance, anomaly detection) with realistic sensor data patterns and equipment hierarchies.

### 4. API Design
RESTful API with clear endpoint structure, comprehensive error handling, and OpenAPI documentation for easy integration.

## 🚧 Roadmap

- [ ] Add authentication and role-based access control
- [ ] Implement WebSocket for real-time data streaming
- [ ] Add support for more agent types (scheduling, optimization)
- [ ] Deploy to Kubernetes with horizontal scaling
- [ ] Add metrics collection with Prometheus/Grafana
- [ ] Implement audit logging for compliance

## 📝 License

MIT License - see LICENSE file for details

## 👤 Author

**Zara Razlan**
- Aspiring AI Engineer with focus on production-grade LLM systems
- Specializing in industrial AI applications and multi-agent workflows

## 🙏 Acknowledgments

- Built as a demonstration of AI engineering capabilities for industrial digitalization
- Inspired by real-world industrial IoT and predictive maintenance use cases
- Architecture informed by best practices in production ML systems

---

**Note**: This is a demonstration project showcasing technical capabilities. For production use, additional security, scalability, and compliance measures would be required.
