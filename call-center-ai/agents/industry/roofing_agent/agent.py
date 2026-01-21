"""Roofing Specialist Agent."""

from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from config import settings
from .tools import roofing_tools
from .prompts import get_roofing_prompt
from loguru import logger


class RoofingAgent:
    """Roofing industry specialist agent."""

    def __init__(self):
        """Initialize Roofing agent."""
        self.model = AnthropicModel(
            "claude-sonnet-4-5-20250929",
            api_key=settings.anthropic_api_key,
        )

        self.agent = Agent(
            model=self.model,
            system_prompt=get_roofing_prompt(),
            tools=roofing_tools,
            retries=2,
        )

        logger.info("RoofingAgent initialized")

    async def handle_query(self, user_input: str, context: dict = None) -> str:
        """Handle roofing-related query."""
        result = await self.agent.run(user_input, deps=context)
        return result.output


# Global instance
roofing_agent = RoofingAgent()
