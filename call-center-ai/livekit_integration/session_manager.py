"""Session manager for handling multiple concurrent LiveKit conversations."""

import asyncio
from typing import Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime

from loguru import logger


@dataclass
class CallSession:
    """Represents an active call session."""

    session_id: str
    participant_id: str
    room_name: str
    industry: str
    role: str
    agent_id: str
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    status: str = "active"  # active, ended, transferred
    metadata: dict = field(default_factory=dict)


class SessionManager:
    """
    Manages multiple concurrent call sessions.

    Handles session lifecycle, load balancing, and session transfer
    between agents when routing is needed.
    """

    def __init__(self, max_concurrent_sessions: int = 10):
        """
        Initialize session manager.

        Args:
            max_concurrent_sessions: Maximum number of concurrent calls
        """
        self.max_concurrent_sessions = max_concurrent_sessions
        self.active_sessions: Dict[str, CallSession] = {}
        self._lock = asyncio.Lock()

        logger.info(
            f"SessionManager initialized with max {max_concurrent_sessions} concurrent sessions"
        )

    async def create_session(
        self,
        session_id: str,
        participant_id: str,
        room_name: str,
        industry: str,
        role: str,
        agent_id: str,
        metadata: Optional[dict] = None,
    ) -> CallSession:
        """
        Create a new call session.

        Args:
            session_id: Unique session identifier
            participant_id: Participant identifier
            room_name: LiveKit room name
            industry: Industry context (hvac, roofing, solar)
            role: Agent role (support, sales, etc.)
            agent_id: Assigned agent ID
            metadata: Additional session metadata

        Returns:
            Created CallSession

        Raises:
            ValueError: If max concurrent sessions exceeded
        """
        async with self._lock:
            if len(self.active_sessions) >= self.max_concurrent_sessions:
                raise ValueError(
                    f"Maximum concurrent sessions ({self.max_concurrent_sessions}) reached"
                )

            session = CallSession(
                session_id=session_id,
                participant_id=participant_id,
                room_name=room_name,
                industry=industry,
                role=role,
                agent_id=agent_id,
                metadata=metadata or {},
            )

            self.active_sessions[session_id] = session

            logger.info(
                f"Session created: {session_id} "
                f"({len(self.active_sessions)}/{self.max_concurrent_sessions} active)"
            )

            return session

    async def end_session(self, session_id: str) -> Optional[CallSession]:
        """
        End a call session.

        Args:
            session_id: Session to end

        Returns:
            Ended session or None if not found
        """
        async with self._lock:
            session = self.active_sessions.pop(session_id, None)

            if session:
                session.end_time = datetime.utcnow()
                session.status = "ended"

                duration = (session.end_time - session.start_time).total_seconds()

                logger.info(
                    f"Session ended: {session_id} "
                    f"(Duration: {duration:.1f}s, "
                    f"{len(self.active_sessions)}/{self.max_concurrent_sessions} active)"
                )

            return session

    async def transfer_session(
        self,
        session_id: str,
        new_agent_id: str,
        new_industry: Optional[str] = None,
        new_role: Optional[str] = None,
    ) -> Optional[CallSession]:
        """
        Transfer session to a different agent.

        Args:
            session_id: Session to transfer
            new_agent_id: Target agent ID
            new_industry: New industry context (optional)
            new_role: New role (optional)

        Returns:
            Updated session or None if not found
        """
        async with self._lock:
            session = self.active_sessions.get(session_id)

            if session:
                old_agent = session.agent_id
                session.agent_id = new_agent_id
                session.status = "transferred"

                if new_industry:
                    session.industry = new_industry
                if new_role:
                    session.role = new_role

                # Track transfer in metadata
                if "transfers" not in session.metadata:
                    session.metadata["transfers"] = []

                session.metadata["transfers"].append(
                    {
                        "from": old_agent,
                        "to": new_agent_id,
                        "timestamp": datetime.utcnow().isoformat(),
                        "industry": session.industry,
                        "role": session.role,
                    }
                )

                logger.info(
                    f"Session transferred: {session_id} "
                    f"from {old_agent} to {new_agent_id} "
                    f"(Industry: {session.industry}, Role: {session.role})"
                )

                # Reset status back to active after transfer
                session.status = "active"

            return session

    def get_session(self, session_id: str) -> Optional[CallSession]:
        """
        Get session by ID.

        Args:
            session_id: Session identifier

        Returns:
            Session or None if not found
        """
        return self.active_sessions.get(session_id)

    def get_active_sessions_count(self) -> int:
        """
        Get count of active sessions.

        Returns:
            Number of active sessions
        """
        return len(self.active_sessions)

    def get_load_percentage(self) -> float:
        """
        Get current load as percentage of max capacity.

        Returns:
            Load percentage (0-100)
        """
        return (len(self.active_sessions) / self.max_concurrent_sessions) * 100

    def can_accept_new_session(self) -> bool:
        """
        Check if new session can be accepted.

        Returns:
            True if capacity available
        """
        return len(self.active_sessions) < self.max_concurrent_sessions

    async def get_all_sessions(self) -> list[CallSession]:
        """
        Get all active sessions.

        Returns:
            List of active sessions
        """
        async with self._lock:
            return list(self.active_sessions.values())

    async def get_sessions_by_industry(self, industry: str) -> list[CallSession]:
        """
        Get sessions for a specific industry.

        Args:
            industry: Industry to filter by

        Returns:
            List of matching sessions
        """
        async with self._lock:
            return [
                session
                for session in self.active_sessions.values()
                if session.industry == industry
            ]

    async def get_sessions_by_role(self, role: str) -> list[CallSession]:
        """
        Get sessions for a specific role.

        Args:
            role: Role to filter by

        Returns:
            List of matching sessions
        """
        async with self._lock:
            return [
                session
                for session in self.active_sessions.values()
                if session.role == role
            ]


# Global session manager instance
session_manager = SessionManager(max_concurrent_sessions=10)
