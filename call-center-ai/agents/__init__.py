"""Agent system - Orchestrator + Industry + Role specialists."""

from .orchestrator import orchestrator, OrchestratorAgent
from .industry.hvac_agent import hvac_agent, HVACAgent
from .industry.roofing_agent import roofing_agent, RoofingAgent
from .industry.solar_agent import solar_agent, SolarAgent
from .role.sales_agent.agent import sales_agent, SalesAgent
from .role.support_agent.agent import support_agent, SupportAgent

__all__ = [
    "orchestrator",
    "OrchestratorAgent",
    "hvac_agent",
    "HVACAgent",
    "roofing_agent",
    "RoofingAgent",
    "solar_agent",
    "SolarAgent",
    "sales_agent",
    "SalesAgent",
    "support_agent",
    "SupportAgent",
]
