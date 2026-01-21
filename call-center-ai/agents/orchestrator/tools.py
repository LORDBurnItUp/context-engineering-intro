"""Tools for the orchestrator agent."""

from typing import Dict, Any, Optional
from pydantic_ai import Tool
from loguru import logger


def analyze_call_context(
    user_input: str,
    call_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Analyze call context to extract key information.

    Args:
        user_input: User's input message
        call_metadata: Optional call metadata

    Returns:
        Analysis of the call context
    """
    analysis = {
        "keywords": [],
        "intent": "unknown",
        "urgency": "normal",
        "sentiment": "neutral",
    }

    # Extract keywords
    input_lower = user_input.lower()

    # Industry keywords
    industry_keywords = {
        "hvac": ["hvac", "heating", "cooling", "air conditioning", "furnace", "ac"],
        "roofing": ["roof", "shingle", "leak", "gutter", "attic"],
        "solar": ["solar", "panel", "renewable", "energy", "battery"],
    }

    for industry, keywords in industry_keywords.items():
        for keyword in keywords:
            if keyword in input_lower:
                analysis["keywords"].append(keyword)
                analysis["suggested_industry"] = industry

    # Intent detection
    if any(word in input_lower for word in ["buy", "purchase", "quote", "price", "cost"]):
        analysis["intent"] = "sales"
    elif any(word in input_lower for word in ["broken", "fix", "repair", "not working", "problem"]):
        analysis["intent"] = "troubleshoot"
    elif any(word in input_lower for word in ["help", "question", "how", "what", "when"]):
        analysis["intent"] = "support"

    # Urgency detection
    if any(word in input_lower for word in ["urgent", "emergency", "asap", "immediately", "now"]):
        analysis["urgency"] = "high"

    # Sentiment detection (basic)
    if any(word in input_lower for word in ["angry", "frustrated", "disappointed", "terrible"]):
        analysis["sentiment"] = "negative"
    elif any(word in input_lower for word in ["happy", "great", "excellent", "thank"]):
        analysis["sentiment"] = "positive"

    logger.info(f"Call context analysis: {analysis}")

    return analysis


def get_agent_availability(industry: str, role: str) -> Dict[str, Any]:
    """
    Check availability of specialist agents.

    Args:
        industry: Industry type
        role: Role type

    Returns:
        Availability information
    """
    # TODO: Implement real availability checking from session manager
    availability = {
        "available": True,
        "current_load": 0,
        "estimated_wait_time": 0,
        "alternative_agents": [],
    }

    logger.info(f"Checking availability for {industry}/{role}: {availability}")

    return availability


def route_to_specialist(
    industry: str,
    role: str,
    session_id: str,
    reasoning: str,
) -> Dict[str, Any]:
    """
    Route call to a specialist agent.

    Args:
        industry: Target industry
        role: Target role
        session_id: Call session ID
        reasoning: Reason for routing

    Returns:
        Routing result
    """
    logger.info(
        f"Routing session {session_id} to {industry}/{role} - Reason: {reasoning}"
    )

    return {
        "routed": True,
        "target_industry": industry,
        "target_role": role,
        "session_id": session_id,
        "reasoning": reasoning,
    }


# Tool definitions for the orchestrator agent
routing_tools = [
    Tool(analyze_call_context, takes_ctx=False),
    Tool(get_agent_availability, takes_ctx=False),
    Tool(route_to_specialist, takes_ctx=False),
]
