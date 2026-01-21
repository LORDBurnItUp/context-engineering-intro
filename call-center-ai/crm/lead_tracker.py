"""Lead tracking and CRM system."""

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
from loguru import logger


class LeadStatus(str, Enum):
    """Lead status categories."""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"
    FOLLOW_UP = "follow_up"


class LeadSource(str, Enum):
    """Lead source types."""
    INBOUND_CALL = "inbound_call"
    OUTBOUND_CALL = "outbound_call"
    WEB_FORM = "web_form"
    REFERRAL = "referral"
    OTHER = "other"


class Lead(BaseModel):
    """Lead model."""
    lead_id: str
    name: str
    phone: str
    email: Optional[str] = None
    industry: str  # hvac, roofing, solar
    source: LeadSource
    status: LeadStatus = LeadStatus.NEW
    assigned_agent: Optional[str] = None
    estimated_value: Optional[float] = None
    notes: List[str] = []
    call_history: List[str] = []
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    next_follow_up: Optional[datetime] = None


class LeadTracker:
    """
    Lead tracking and CRM system.

    Manages leads through the sales pipeline.
    """

    def __init__(self):
        """Initialize lead tracker."""
        self.leads: dict[str, Lead] = {}
        logger.info("LeadTracker initialized")

    async def create_lead(
        self,
        lead_id: str,
        name: str,
        phone: str,
        industry: str,
        source: LeadSource,
        **kwargs
    ) -> Lead:
        """
        Create a new lead.

        Args:
            lead_id: Unique lead identifier
            name: Lead name
            phone: Phone number
            industry: Industry type
            source: Lead source
            **kwargs: Additional lead attributes

        Returns:
            Created Lead
        """
        lead = Lead(
            lead_id=lead_id,
            name=name,
            phone=phone,
            industry=industry,
            source=source,
            **kwargs
        )

        self.leads[lead_id] = lead
        logger.info(f"Lead created: {lead_id} - {name} ({industry})")

        return lead

    async def update_lead_status(
        self,
        lead_id: str,
        status: LeadStatus,
        note: Optional[str] = None,
    ) -> Optional[Lead]:
        """
        Update lead status.

        Args:
            lead_id: Lead identifier
            status: New status
            note: Optional note about status change

        Returns:
            Updated Lead or None if not found
        """
        lead = self.leads.get(lead_id)

        if not lead:
            logger.warning(f"Lead not found: {lead_id}")
            return None

        old_status = lead.status
        lead.status = status
        lead.updated_at = datetime.utcnow()

        if note:
            lead.notes.append(f"[{datetime.utcnow().isoformat()}] Status: {old_status} -> {status}. {note}")

        logger.info(f"Lead status updated: {lead_id} - {old_status} -> {status}")

        return lead

    async def add_call_to_lead(
        self,
        lead_id: str,
        session_id: str,
        outcome: str,
    ) -> Optional[Lead]:
        """
        Add call record to lead.

        Args:
            lead_id: Lead identifier
            session_id: Call session ID
            outcome: Call outcome

        Returns:
            Updated Lead or None if not found
        """
        lead = self.leads.get(lead_id)

        if not lead:
            logger.warning(f"Lead not found: {lead_id}")
            return None

        call_record = f"[{datetime.utcnow().isoformat()}] Call {session_id}: {outcome}"
        lead.call_history.append(call_record)
        lead.updated_at = datetime.utcnow()

        logger.info(f"Call added to lead: {lead_id} - {outcome}")

        return lead

    async def get_leads_by_status(self, status: LeadStatus) -> List[Lead]:
        """
        Get all leads with specific status.

        Args:
            status: Lead status to filter by

        Returns:
            List of matching leads
        """
        return [lead for lead in self.leads.values() if lead.status == status]

    async def get_leads_needing_follow_up(self) -> List[Lead]:
        """
        Get leads that need follow-up.

        Returns:
            List of leads needing follow-up
        """
        now = datetime.utcnow()
        return [
            lead for lead in self.leads.values()
            if lead.next_follow_up and lead.next_follow_up <= now
        ]

    async def get_pipeline_summary(self) -> dict:
        """
        Get sales pipeline summary.

        Returns:
            Pipeline statistics
        """
        summary = {
            "total_leads": len(self.leads),
            "by_status": {},
            "by_industry": {},
            "total_estimated_value": 0.0,
        }

        for lead in self.leads.values():
            # Count by status
            status_key = lead.status.value
            summary["by_status"][status_key] = summary["by_status"].get(status_key, 0) + 1

            # Count by industry
            summary["by_industry"][lead.industry] = summary["by_industry"].get(lead.industry, 0) + 1

            # Sum estimated value
            if lead.estimated_value:
                summary["total_estimated_value"] += lead.estimated_value

        return summary


# Global lead tracker instance
lead_tracker = LeadTracker()
