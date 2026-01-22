import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from typing import List, Dict, Any, Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class RAGPipeline:
    """RAG pipeline for industrial documentation."""
    
    def __init__(self):
        """Initialize RAG pipeline with ChromaDB."""
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.Client(
            ChromaSettings(
                persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                anonymized_telemetry=False
            )
        )
        
        # Initialize vector store
        self.vectorstore = Chroma(
            client=self.chroma_client,
            collection_name=settings.COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY
        )
        
        # Text splitter for document chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        logger.info("RAG Pipeline initialized successfully")
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents with 'content' and 'metadata'
        """
        try:
            texts = []
            metadatas = []
            
            for doc in documents:
                # Split document into chunks
                chunks = self.text_splitter.split_text(doc["content"])
                texts.extend(chunks)
                
                # Add metadata to each chunk
                for _ in chunks:
                    metadatas.append({
                        **doc.get("metadata", {}),
                        "source": doc.get("source", "unknown")
                    })
            
            # Add to vector store
            self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
            logger.info(f"Added {len(texts)} chunks from {len(documents)} documents")
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def search(
        self, 
        query: str, 
        k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_dict: Metadata filters
            
        Returns:
            List of relevant documents with content and metadata
        """
        try:
            # Perform similarity search
            if filter_dict:
                results = self.vectorstore.similarity_search(
                    query, 
                    k=k,
                    filter=filter_dict
                )
            else:
                results = self.vectorstore.similarity_search(query, k=k)
            
            # Format results
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "source": doc.metadata.get("source", "unknown")
                })
            
            logger.info(f"Retrieved {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    def search_equipment_docs(
        self, 
        query: str, 
        equipment_id: Optional[str] = None,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search equipment-specific documentation.
        
        Args:
            query: Search query
            equipment_id: Filter by equipment ID
            k: Number of results
            
        Returns:
            Relevant equipment documentation
        """
        filter_dict = {"equipment_id": equipment_id} if equipment_id else None
        return self.search(query, k=k, filter_dict=filter_dict)
    
    def get_context_for_query(
        self, 
        query: str,
        equipment_id: Optional[str] = None
    ) -> str:
        """
        Get formatted context for LLM query.
        
        Args:
            query: User query
            equipment_id: Equipment ID filter
            
        Returns:
            Formatted context string
        """
        results = self.search_equipment_docs(query, equipment_id, k=3)
        
        if not results:
            return "No relevant documentation found."
        
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"Document {i} (Source: {result['source']}):\n"
                f"{result['content']}\n"
            )
        
        return "\n".join(context_parts)


# Global RAG pipeline instance
rag_pipeline: Optional[RAGPipeline] = None


def get_rag_pipeline() -> RAGPipeline:
    """Get or create RAG pipeline instance."""
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline
