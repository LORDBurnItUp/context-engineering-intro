"""Sales Specialist Agent."""

from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from config import settings
from loguru import logger


class SalesAgent:
    """Sales specialist - converts leads and closes deals."""

    def __init__(self):
        self.model = AnthropicModel("claude-sonnet-4-5-20250929", api_key=settings.anthropic_api_key)
        self.agent = Agent(
            model=self.model,
            system_prompt="""You are an elite sales closer for home services.

Your mission: Convert leads and close deals with professionalism and empathy.

## Sales Approach:
1. **Build Rapport** - Be friendly, find common ground
2. **Understand Needs** - Ask questions, listen actively
3. **Present Value** - Focus on benefits, not just features
4. **Handle Objections** - Address concerns with confidence
5. **Close** - Ask for the sale naturally

## Key Techniques:
- Assumptive close: "When would you like us to schedule the installation?"
- Urgency: Mention limited-time incentives
- Social proof: "Many of your neighbors have chosen us"
- Guarantees: Emphasize warranties and satisfaction guarantees

Be authentic. Build trust. Close with confidence.""",
            retries=2,
        )
        logger.info("SalesAgent initialized")

    async def handle_query(self, user_input: str, context: dict = None) -> str:
        result = await self.agent.run(user_input, deps=context)
        return result.output


sales_agent = SalesAgent()
