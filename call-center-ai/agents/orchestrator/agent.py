"""Orchestrator Agent - Routes calls to specialized agents."""

from typing import Optional, Dict, Any
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.anthropic import AnthropicModel

from config import settings
from .tools import routing_tools
from .prompts import get_orchestrator_prompt
from loguru import logger


class OrchestratorAgent:
    """
    Master orchestrator that routes calls to appropriate specialist agents.

    The orchestrator:
    - Analyzes incoming call context
    - Determines the best industry specialist (HVAC, Roofing, Solar)
    - Determines the best role (Support, Sales, Troubleshoot, Cold Call)
    - Routes the call appropriately
    - Handles agent transfers when needed
    - Monitors agent performance
    """

    def __init__(self):
        """Initialize the orchestrator agent."""
        # Use Haiku for fast routing decisions
        self.model = AnthropicModel(
            "claude-haiku-4-5-20250925",
            api_key=settings.anthropic_api_key,
        )

        # Create the agent with routing tools
        self.agent = Agent(
            model=self.model,
            system_prompt=get_orchestrator_prompt(),
            tools=routing_tools,
            retries=2,
        )

        logger.info("OrchestratorAgent initialized")

    async def route_call(
        self,
        user_input: str,
        call_metadata: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Route a call to the appropriate specialist agent.

        Args:
            user_input: User's input message
            call_metadata: Metadata about the call (caller info, etc.)
            conversation_history: Previous conversation turns

        Returns:
            Routing decision with industry, role, and transfer reason
        """
        # Build context for routing decision
        context = self._build_routing_context(
            user_input, call_metadata, conversation_history
        )

        logger.info(f"Routing call with context: {context}")

        try:
            # Run the agent to make routing decision
            result = await self.agent.run(
                f"""Analyze this call and determine the best routing:

User Input: {user_input}

Call Metadata: {call_metadata or 'None'}

Conversation History: {conversation_history or 'None'}

Determine:
1. Industry specialist needed (hvac, roofing, solar, or general)
2. Role type needed (support, sales, troubleshoot, cold_call)
3. Confidence level (0-100)
4. Reasoning for the routing decision

Respond with your routing decision and reasoning."""
            )

            routing_decision = self._parse_routing_decision(result)

            logger.info(f"Routing decision: {routing_decision}")

            return routing_decision

        except Exception as e:
            logger.error(f"Error in routing: {e}")
            # Default to general support on error
            return {
                "industry": "general",
                "role": "support",
                "confidence": 0,
                "reasoning": f"Error in routing: {str(e)}",
                "transfer_needed": False,
            }

    async def should_transfer(
        self,
        current_industry: str,
        current_role: str,
        user_input: str,
        conversation_history: list,
    ) -> Dict[str, Any]:
        """
        Determine if a call should be transferred to a different agent.

        Args:
            current_industry: Current industry specialist
            current_role: Current role
            user_input: Latest user input
            conversation_history: Previous conversation

        Returns:
            Transfer decision with new routing if transfer needed
        """
        try:
            result = await self.agent.run(
                f"""Analyze if this call needs to be transferred to a different agent:

Current Agent: Industry={current_industry}, Role={current_role}

Latest User Input: {user_input}

Conversation History: {conversation_history[-5:] if len(conversation_history) > 5 else conversation_history}

Should this call be transferred? Consider:
1. Is the current agent capable of handling this?
2. Would a different specialist be better?
3. Has the conversation topic changed?

Respond with transfer decision and reasoning."""
            )

            transfer_decision = self._parse_transfer_decision(result)

            logger.info(f"Transfer decision: {transfer_decision}")

            return transfer_decision

        except Exception as e:
            logger.error(f"Error in transfer decision: {e}")
            return {
                "transfer_needed": False,
                "reasoning": f"Error: {str(e)}",
            }

    def _build_routing_context(
        self,
        user_input: str,
        call_metadata: Optional[Dict[str, Any]],
        conversation_history: Optional[list],
    ) -> Dict[str, Any]:
        """Build context for routing decision."""
        return {
            "user_input": user_input,
            "metadata": call_metadata or {},
            "history_length": len(conversation_history) if conversation_history else 0,
            "has_metadata": bool(call_metadata),
        }

    def _parse_routing_decision(self, result) -> Dict[str, Any]:
        """
        Parse the agent's routing decision.

        Args:
            result: Agent run result

        Returns:
            Structured routing decision
        """
        # Extract the routing decision from agent output
        # For now, use simple text parsing - can enhance with structured output
        output = str(result.output).lower()

        # Detect industry
        industry = "general"
        if "hvac" in output or "heating" in output or "cooling" in output or "air conditioning" in output:
            industry = "hvac"
        elif "roof" in output or "shingle" in output or "leak" in output:
            industry = "roofing"
        elif "solar" in output or "panel" in output or "renewable" in output:
            industry = "solar"

        # Detect role
        role = "support"
        if "sales" in output or "buy" in output or "purchase" in output or "price" in output:
            role = "sales"
        elif "troubleshoot" in output or "repair" in output or "fix" in output or "broken" in output:
            role = "troubleshoot"
        elif "cold call" in output or "outbound" in output:
            role = "cold_call"

        # Estimate confidence
        confidence = 80  # Default confidence
        if "high confidence" in output or "definitely" in output or "clearly" in output:
            confidence = 95
        elif "low confidence" in output or "unsure" in output or "maybe" in output:
            confidence = 50

        return {
            "industry": industry,
            "role": role,
            "confidence": confidence,
            "reasoning": str(result.output),
            "transfer_needed": False,
        }

    def _parse_transfer_decision(self, result) -> Dict[str, Any]:
        """
        Parse the agent's transfer decision.

        Args:
            result: Agent run result

        Returns:
            Structured transfer decision
        """
        output = str(result.output).lower()

        transfer_needed = (
            "transfer" in output
            or "switch" in output
            or "different agent" in output
            or "better suited" in output
        )

        return {
            "transfer_needed": transfer_needed,
            "reasoning": str(result.output),
        }

    async def get_agent_performance_summary(self) -> Dict[str, Any]:
        """
        Get performance summary of all agents.

        Returns:
            Performance metrics for each agent type
        """
        # TODO: Implement performance tracking
        return {
            "total_calls": 0,
            "by_industry": {
                "hvac": 0,
                "roofing": 0,
                "solar": 0,
            },
            "by_role": {
                "support": 0,
                "sales": 0,
                "troubleshoot": 0,
                "cold_call": 0,
            },
        }


# Global orchestrator instance
orchestrator = OrchestratorAgent()
