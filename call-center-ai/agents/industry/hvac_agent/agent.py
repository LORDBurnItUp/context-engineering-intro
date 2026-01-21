"""HVAC Specialist Agent."""

from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from config import settings
from .tools import hvac_tools
from .prompts import get_hvac_prompt
from loguru import logger


class HVACAgent:
    """
    HVAC industry specialist agent.

    Handles:
    - HVAC system questions
    - Heating and cooling issues
    - Maintenance and installation
    - Energy efficiency
    """

    def __init__(self):
        """Initialize HVAC agent."""
        self.model = AnthropicModel(
            "claude-sonnet-4-5-20250929",
            api_key=settings.anthropic_api_key,
        )

        self.agent = Agent(
            model=self.model,
            system_prompt=get_hvac_prompt(),
            tools=hvac_tools,
            retries=2,
        )

        logger.info("HVACAgent initialized")

    async def handle_query(self, user_input: str, context: dict = None) -> str:
        """
        Handle HVAC-related query.

        Args:
            user_input: User's question/request
            context: Additional context (RAG results, history, etc.)

        Returns:
            Agent response
        """
        result = await self.agent.run(user_input, deps=context)
        return result.output


# Global instance
hvac_agent = HVACAgent()
