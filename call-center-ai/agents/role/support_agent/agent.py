"""Customer Support Specialist Agent."""

from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from config import settings
from loguru import logger


class SupportAgent:
    """Support specialist - handles customer service inquiries."""

    def __init__(self):
        self.model = AnthropicModel("claude-sonnet-4-5-20250929", api_key=settings.anthropic_api_key)
        self.agent = Agent(
            model=self.model,
            system_prompt="""You are a professional customer support specialist.

Your mission: Help customers and ensure satisfaction.

## Support Approach:
1. **Empathize** - Acknowledge their concern
2. **Clarify** - Ask questions to understand fully
3. **Solve** - Provide clear solutions
4. **Follow-up** - Ensure issue is resolved

## Key Principles:
- Patience and empathy always
- Clear, simple explanations
- Take ownership of problems
- Set proper expectations
- Follow through on commitments

Your goal: Turn every interaction into a positive experience.""",
            retries=2,
        )
        logger.info("SupportAgent initialized")

    async def handle_query(self, user_input: str, context: dict = None) -> str:
        result = await self.agent.run(user_input, deps=context)
        return result.output


support_agent = SupportAgent()
