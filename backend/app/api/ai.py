from fastapi import APIRouter, HTTPException
from typing import Optional
import logging

from app.models.schemas import QueryRequest, QueryResponse
from app.agents.orchestrator import get_orchestrator

router = APIRouter(prefix="/ai", tags=["ai"])
logger = logging.getLogger(__name__)


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process an AI query using multi-agent system.
    
    The query will be routed through appropriate agents:
    - Analysis Agent: Analyzes equipment data and identifies issues
    - Retrieval Agent: Searches documentation using RAG
    - Recommendation Agent: Provides actionable recommendations
    """
    try:
        orchestrator = get_orchestrator()
        
        result = orchestrator.process_query(
            query=request.query,
            equipment_id=request.equipment_id
        )
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/health")
async def ai_health_check():
    """Check if AI services are operational."""
    try:
        orchestrator = get_orchestrator()
        return {
            "status": "healthy",
            "message": "AI services operational"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "message": str(e)
        }
