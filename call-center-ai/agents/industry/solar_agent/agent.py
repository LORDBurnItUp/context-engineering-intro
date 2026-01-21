"""Solar Energy Specialist Agent."""

from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from config import settings
from .tools import solar_tools
from .prompts import get_solar_prompt
from loguru import logger


class SolarAgent:
    """Solar energy industry specialist agent."""

    def __init__(self):
        """Initialize Solar agent."""
        self.model = AnthropicModel(
            "claude-sonnet-4-5-20250929",
            api_key=settings.anthropic_api_key,
        )

        self.agent = Agent(
            model=self.model,
            system_prompt=get_solar_prompt(),
            tools=solar_tools,
            retries=2,
        )

        logger.info("SolarAgent initialized")

    async def handle_query(self, user_input: str, context: dict = None) -> str:
        """Handle solar-related query."""
        result = await self.agent.run(user_input, deps=context)
        return result.output


# Global instance
solar_agent = SolarAgent()
