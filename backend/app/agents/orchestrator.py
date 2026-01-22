from typing import TypedDict, Annotated, Sequence
import operator
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation
import logging

from app.core.config import settings
from app.rag.pipeline import get_rag_pipeline

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """State for multi-agent workflow."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    equipment_id: str | None
    analysis_result: str | None
    retrieved_docs: list | None
    recommendations: list | None
    next_agent: str | None


class IndustrialAgentOrchestrator:
    """Multi-agent orchestrator for industrial AI queries."""
    
    def __init__(self):
        """Initialize the agent orchestrator."""
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.AGENT_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.rag_pipeline = get_rag_pipeline()
        self.workflow = self._build_workflow()
        logger.info("Agent orchestrator initialized")
    
    def _build_workflow(self) -> StateGraph:
        """Build the multi-agent workflow graph."""
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("router", self._router_agent)
        workflow.add_node("analysis", self._analysis_agent)
        workflow.add_node("retrieval", self._retrieval_agent)
        workflow.add_node("recommendation", self._recommendation_agent)
        workflow.add_node("synthesizer", self._synthesizer_agent)
        
        # Define workflow edges
        workflow.set_entry_point("router")
        
        # Router decides which agent to use first
        workflow.add_conditional_edges(
            "router",
            self._route_decision,
            {
                "analysis": "analysis",
                "retrieval": "retrieval",
                "direct_answer": "synthesizer"
            }
        )
        
        # Analysis can lead to retrieval or recommendations
        workflow.add_conditional_edges(
            "analysis",
            self._after_analysis,
            {
                "retrieval": "retrieval",
                "recommendation": "recommendation"
            }
        )
        
        # Retrieval leads to recommendations
        workflow.add_edge("retrieval", "recommendation")
        
        # Recommendations lead to synthesis
        workflow.add_edge("recommendation", "synthesizer")
        
        # Synthesizer is the end
        workflow.add_edge("synthesizer", END)
        
        return workflow.compile()
    
    def _router_agent(self, state: AgentState) -> AgentState:
        """Route query to appropriate agent."""
        query = state["query"].lower()
        
        # Determine routing based on query type
        if any(word in query for word in ["why", "cause", "analyze", "explain"]):
            state["next_agent"] = "analysis"
        elif any(word in query for word in ["manual", "documentation", "procedure", "history"]):
            state["next_agent"] = "retrieval"
        else:
            state["next_agent"] = "analysis"
        
        logger.info(f"Router: Directing to {state['next_agent']} agent")
        return state
    
    def _route_decision(self, state: AgentState) -> str:
        """Decision function for routing."""
        return state.get("next_agent", "analysis")
    
    def _analysis_agent(self, state: AgentState) -> AgentState:
        """Analyze equipment data and identify issues."""
        system_prompt = """You are an expert industrial equipment analyst. 
        Analyze the query and equipment data to identify issues, patterns, and anomalies.
        Provide clear, technical analysis focusing on root causes and operational impacts."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Query: {state['query']}\n\nProvide your analysis.")
        ]
        
        response = self.llm.invoke(messages)
        state["analysis_result"] = response.content
        state["messages"].append(AIMessage(content=f"Analysis: {response.content}"))
        
        logger.info("Analysis agent completed")
        return state
    
    def _after_analysis(self, state: AgentState) -> str:
        """Decide next step after analysis."""
        query = state["query"].lower()
        if any(word in query for word in ["manual", "documentation", "procedure"]):
            return "retrieval"
        return "recommendation"
    
    def _retrieval_agent(self, state: AgentState) -> AgentState:
        """Retrieve relevant documentation using RAG."""
        query = state["query"]
        equipment_id = state.get("equipment_id")
        
        # Retrieve relevant documents
        docs = self.rag_pipeline.search_equipment_docs(
            query=query,
            equipment_id=equipment_id,
            k=3
        )
        
        state["retrieved_docs"] = docs
        
        # Summarize retrieved information
        if docs:
            doc_summary = "\n\n".join([
                f"Source: {doc['source']}\n{doc['content'][:300]}..."
                for doc in docs
            ])
            state["messages"].append(
                AIMessage(content=f"Retrieved Documentation:\n{doc_summary}")
            )
        
        logger.info(f"Retrieval agent found {len(docs)} documents")
        return state
    
    def _recommendation_agent(self, state: AgentState) -> AgentState:
        """Generate actionable recommendations."""
        system_prompt = """You are an expert maintenance advisor for industrial equipment.
        Based on the analysis and documentation, provide specific, actionable recommendations.
        Format recommendations as a numbered list. Be concise and practical."""
        
        context_parts = [f"Query: {state['query']}"]
        
        if state.get("analysis_result"):
            context_parts.append(f"\nAnalysis: {state['analysis_result']}")
        
        if state.get("retrieved_docs"):
            doc_context = "\n".join([
                f"- {doc['source']}: {doc['content'][:200]}"
                for doc in state["retrieved_docs"][:2]
            ])
            context_parts.append(f"\nRelevant Documentation:\n{doc_context}")
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content="\n".join(context_parts))
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse recommendations
        recommendations = [
            line.strip() 
            for line in response.content.split("\n") 
            if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith("-"))
        ]
        
        state["recommendations"] = recommendations
        state["messages"].append(
            AIMessage(content=f"Recommendations:\n{response.content}")
        )
        
        logger.info(f"Recommendation agent generated {len(recommendations)} recommendations")
        return state
    
    def _synthesizer_agent(self, state: AgentState) -> AgentState:
        """Synthesize final response."""
        system_prompt = """You are a helpful AI assistant synthesizing information.
        Create a clear, concise final answer that combines analysis, documentation, and recommendations.
        Format your response in a user-friendly way."""
        
        synthesis_context = f"Original Query: {state['query']}\n\n"
        
        if state.get("analysis_result"):
            synthesis_context += f"Analysis: {state['analysis_result']}\n\n"
        
        if state.get("recommendations"):
            synthesis_context += "Recommendations:\n" + "\n".join(state["recommendations"])
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=synthesis_context)
        ]
        
        response = self.llm.invoke(messages)
        state["messages"].append(AIMessage(content=f"Final Answer: {response.content}"))
        
        logger.info("Synthesizer agent completed")
        return state
    
    def process_query(
        self, 
        query: str, 
        equipment_id: str | None = None
    ) -> dict:
        """
        Process a query through the multi-agent system.
        
        Args:
            query: User query
            equipment_id: Optional equipment ID for context
            
        Returns:
            Response with answer, sources, and recommendations
        """
        try:
            # Initialize state
            initial_state = {
                "messages": [HumanMessage(content=query)],
                "query": query,
                "equipment_id": equipment_id,
                "analysis_result": None,
                "retrieved_docs": None,
                "recommendations": None,
                "next_agent": None
            }
            
            # Run workflow
            final_state = self.workflow.invoke(initial_state)
            
            # Extract final answer
            final_message = [
                msg.content for msg in final_state["messages"] 
                if isinstance(msg, AIMessage) and "Final Answer:" in msg.content
            ]
            
            answer = final_message[-1].replace("Final Answer: ", "") if final_message else "Unable to process query."
            
            # Compile sources
            sources = []
            if final_state.get("retrieved_docs"):
                sources = [doc["source"] for doc in final_state["retrieved_docs"]]
            
            # Get recommendations
            recommendations = final_state.get("recommendations", [])
            
            return {
                "answer": answer,
                "sources": sources,
                "recommendations": recommendations,
                "confidence": 0.85,
                "agent_reasoning": self._extract_reasoning(final_state)
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "answer": "I encountered an error processing your query. Please try again.",
                "sources": [],
                "recommendations": [],
                "confidence": 0.0,
                "agent_reasoning": str(e)
            }
    
    def _extract_reasoning(self, state: AgentState) -> str:
        """Extract agent reasoning chain."""
        reasoning_parts = []
        
        if state.get("analysis_result"):
            reasoning_parts.append(f"Analysis: {state['analysis_result'][:200]}...")
        
        if state.get("retrieved_docs"):
            reasoning_parts.append(f"Retrieved {len(state['retrieved_docs'])} relevant documents")
        
        if state.get("recommendations"):
            reasoning_parts.append(f"Generated {len(state['recommendations'])} recommendations")
        
        return " → ".join(reasoning_parts) if reasoning_parts else "Direct response"


# Global orchestrator instance
orchestrator: IndustrialAgentOrchestrator | None = None


def get_orchestrator() -> IndustrialAgentOrchestrator:
    """Get or create orchestrator instance."""
    global orchestrator
    if orchestrator is None:
        orchestrator = IndustrialAgentOrchestrator()
    return orchestrator
