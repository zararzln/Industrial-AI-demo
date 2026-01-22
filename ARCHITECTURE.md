# System Architecture

## High-Level Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[React UI]
        Executive[Executive Dashboard]
        Operator[Operator Dashboard]
    end
    
    subgraph "API Layer"
        API[FastAPI Backend]
        Equipment[Equipment API]
        Dashboard[Dashboard API]
        AI[AI API]
    end
    
    subgraph "Service Layer"
        DataService[Data Service]
        RAG[RAG Pipeline]
        Orchestrator[Multi-Agent Orchestrator]
    end
    
    subgraph "Agent Layer"
        Router[Router Agent]
        Analysis[Analysis Agent]
        Retrieval[Retrieval Agent]
        Recommendation[Recommendation Agent]
        Synthesizer[Synthesizer Agent]
    end
    
    subgraph "Data Layer"
        Equipment DB[(Equipment Data)]
        Vector[(ChromaDB)]
        OpenAI[OpenAI GPT-4]
    end
    
    UI --> Executive
    UI --> Operator
    Executive --> API
    Operator --> API
    
    API --> Equipment
    API --> Dashboard
    API --> AI
    
    Equipment --> DataService
    Dashboard --> DataService
    AI --> Orchestrator
    
    Orchestrator --> Router
    Router --> Analysis
    Router --> Retrieval
    Analysis --> Recommendation
    Retrieval --> Recommendation
    Recommendation --> Synthesizer
    
    DataService --> Equipment DB
    Retrieval --> RAG
    RAG --> Vector
    Analysis --> OpenAI
    Retrieval --> OpenAI
    Recommendation --> OpenAI
    Synthesizer --> OpenAI
```

## Multi-Agent Workflow

```mermaid
stateDiagram-v2
    [*] --> Router: User Query
    
    Router --> Analysis: Analyze Request
    Router --> Retrieval: Documentation Query
    Router --> Synthesizer: Simple Query
    
    Analysis --> Retrieval: Need Docs
    Analysis --> Recommendation: Have Analysis
    
    Retrieval --> Recommendation: With Context
    
    Recommendation --> Synthesizer: Final Synthesis
    
    Synthesizer --> [*]: Response
```

## Data Flow - AI Query Processing

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Orchestrator
    participant Agents
    participant RAG
    participant LLM
    
    User->>Frontend: Ask Question
    Frontend->>API: POST /ai/query
    API->>Orchestrator: Process Query
    
    Orchestrator->>Agents: Route to Router
    Agents->>Agents: Analyze Query Type
    
    alt Need Analysis
        Agents->>LLM: Analyze Equipment Data
        LLM-->>Agents: Analysis Result
    end
    
    alt Need Documentation
        Agents->>RAG: Search Vector Store
        RAG-->>Agents: Relevant Docs
        Agents->>LLM: Context + Query
        LLM-->>Agents: Contextualized Response
    end
    
    Agents->>LLM: Generate Recommendations
    LLM-->>Agents: Action Items
    
    Agents->>LLM: Synthesize Final Answer
    LLM-->>Agents: Complete Response
    
    Agents-->>Orchestrator: Compiled Result
    Orchestrator-->>API: Response Object
    API-->>Frontend: JSON Response
    Frontend-->>User: Display Answer
```

## Component Architecture

### Backend Components

```
backend/
├── app/
│   ├── agents/           # Multi-agent orchestration
│   │   └── orchestrator.py
│   ├── api/              # REST API endpoints
│   │   ├── equipment.py
│   │   ├── dashboard.py
│   │   └── ai.py
│   ├── core/             # Configuration
│   │   └── config.py
│   ├── models/           # Data models
│   │   └── schemas.py
│   ├── rag/              # RAG pipeline
│   │   └── pipeline.py
│   ├── services/         # Business logic
│   │   └── data_service.py
│   └── main.py           # FastAPI app
├── scripts/              # Utility scripts
│   └── seed_data.py
└── tests/                # Test suite
```

### Frontend Components

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   ├── views/            # Page components
│   │   ├── ExecutiveDashboard.tsx
│   │   └── OperatorDashboard.tsx
│   ├── services/         # API integration
│   │   └── api.ts
│   └── App.tsx           # Main application
```

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **AI Orchestration**: LangGraph
- **Vector Store**: ChromaDB
- **LLM**: OpenAI GPT-4
- **Data Validation**: Pydantic

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions

## Key Design Patterns

### 1. Multi-Agent Pattern
Each agent has a specific responsibility:
- **Router**: Determines query type and routing
- **Analysis**: Analyzes equipment data and metrics
- **Retrieval**: Searches documentation using RAG
- **Recommendation**: Generates actionable advice
- **Synthesizer**: Compiles final response

### 2. RAG Pipeline
Retrieval-Augmented Generation for documentation:
1. Documents chunked and embedded
2. Stored in vector database
3. Semantic search on queries
4. Context provided to LLM

### 3. Service Layer Pattern
Business logic separated from API layer:
- Data Service handles equipment data
- RAG Pipeline manages documentation
- Orchestrator coordinates agents

### 4. Dual View Pattern
Two interfaces for different users:
- Executive: Strategic overview, KPIs
- Operator: Tactical details, AI assistant
