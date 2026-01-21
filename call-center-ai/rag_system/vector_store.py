"""Vector store for RAG system using ChromaDB."""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from config import settings
from loguru import logger


class VectorStore:
    """
    Vector database for storing and retrieving conversation context.

    Uses ChromaDB for fast vector similarity search.
    """

    def __init__(self):
        """Initialize ChromaDB client."""
        try:
            self.client = chromadb.HttpClient(
                host=settings.chroma_host,
                port=settings.chroma_port,
            )
            logger.info(f"Connected to ChromaDB at {settings.chroma_host}:{settings.chroma_port}")
        except Exception as e:
            logger.warning(f"Failed to connect to ChromaDB: {e}. Using in-memory DB.")
            self.client = chromadb.Client(ChromaSettings(anonymized_telemetry=False))

        # Create collections
        self.conversations = self._get_or_create_collection("conversations")
        self.knowledge_base = self._get_or_create_collection("knowledge_base")
        self.successful_calls = self._get_or_create_collection("successful_calls")

    def _get_or_create_collection(self, name: str):
        """Get or create a collection."""
        try:
            return self.client.get_or_create_collection(name=name)
        except Exception as e:
            logger.error(f"Error creating collection {name}: {e}")
            return None

    async def store_conversation(
        self,
        session_id: str,
        messages: List[Dict[str, str]],
        metadata: Dict[str, Any],
    ):
        """
        Store conversation for later retrieval.

        Args:
            session_id: Unique session identifier
            messages: List of conversation messages
            metadata: Session metadata (industry, role, outcome, etc.)
        """
        if not self.conversations:
            return

        # Combine messages into a single document
        conversation_text = "\n".join(
            [f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in messages]
        )

        try:
            self.conversations.add(
                documents=[conversation_text],
                metadatas=[metadata],
                ids=[session_id],
            )
            logger.info(f"Stored conversation: {session_id}")
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")

    async def retrieve_similar_conversations(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        n_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve similar past conversations.

        Args:
            query: Query text for similarity search
            filters: Optional metadata filters
            n_results: Number of results to return

        Returns:
            List of similar conversations with metadata
        """
        if not self.conversations:
            return []

        try:
            results = self.conversations.query(
                query_texts=[query],
                n_results=n_results,
                where=filters,
            )

            return [
                {
                    "content": doc,
                    "metadata": meta,
                    "similarity": 1 - dist,  # Convert distance to similarity
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                )
            ]
        except Exception as e:
            logger.error(f"Error retrieving conversations: {e}")
            return []

    async def store_knowledge(
        self,
        knowledge_id: str,
        content: str,
        category: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Store knowledge base content.

        Args:
            knowledge_id: Unique identifier
            content: Knowledge content
            category: Category (hvac, roofing, solar, general)
            metadata: Additional metadata
        """
        if not self.knowledge_base:
            return

        meta = {"category": category, **(metadata or {})}

        try:
            self.knowledge_base.add(
                documents=[content],
                metadatas=[meta],
                ids=[knowledge_id],
            )
            logger.info(f"Stored knowledge: {knowledge_id} ({category})")
        except Exception as e:
            logger.error(f"Error storing knowledge: {e}")

    async def retrieve_knowledge(
        self,
        query: str,
        category: Optional[str] = None,
        n_results: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant knowledge from knowledge base.

        Args:
            query: Query text
            category: Optional category filter
            n_results: Number of results

        Returns:
            List of relevant knowledge chunks
        """
        if not self.knowledge_base:
            return []

        filters = {"category": category} if category else None

        try:
            results = self.knowledge_base.query(
                query_texts=[query],
                n_results=n_results,
                where=filters,
            )

            return [
                {
                    "content": doc,
                    "metadata": meta,
                    "relevance": 1 - dist,
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                )
            ]
        except Exception as e:
            logger.error(f"Error retrieving knowledge: {e}")
            return []


# Global vector store instance
vector_store = VectorStore()
