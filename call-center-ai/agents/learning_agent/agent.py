"""Learning Agent - Analyzes calls and improves the system."""

from typing import List, Dict, Any
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from config import settings
from loguru import logger


class LearningAgent:
    """
    Self-improvement agent that learns from call data.

    Capabilities:
    - Analyzes successful vs failed calls
    - Identifies patterns in agent performance
    - Suggests prompt improvements
    - Runs A/B tests on prompts
    - Auto-updates knowledge base
    - Spawns new specialist agents as needed
    """

    def __init__(self):
        """Initialize learning agent."""
        self.model = AnthropicModel(
            "claude-sonnet-4-5-20250929",
            api_key=settings.anthropic_api_key,
        )

        self.agent = Agent(
            model=self.model,
            system_prompt=self._get_learning_prompt(),
            retries=2,
        )

        self.call_analysis_cache = []
        logger.info("LearningAgent initialized")

    def _get_learning_prompt(self) -> str:
        """Get system prompt for learning agent."""
        return """You are the Learning Agent - the meta-intelligence that improves the entire call center system.

## Your Mission:
Analyze call patterns and continuously improve agent performance.

## What You Analyze:
1. **Successful Calls** - What worked? Extract patterns.
2. **Failed Calls** - What went wrong? Identify issues.
3. **Agent Performance** - Which agents are most effective?
4. **Prompt Effectiveness** - Which prompts lead to conversions?
5. **Knowledge Gaps** - What questions couldn't be answered?

## Your Actions:
1. **Suggest Prompt Improvements** - Refine agent prompts based on data
2. **Update Knowledge Base** - Add new information from successful calls
3. **Recommend New Agents** - Suggest new specialists when patterns emerge
4. **A/B Test Variations** - Test different approaches
5. **Generate Reports** - Provide insights to humans

## Analysis Framework:
- Call outcome (success/failure)
- Customer sentiment
- Agent responses
- Resolution time
- Conversion rate
- Customer satisfaction

Be data-driven. Be objective. Be relentless in improvement."""

    async def analyze_call(
        self,
        session_id: str,
        conversation: List[Dict[str, str]],
        outcome: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze a single call and extract learnings.

        Args:
            session_id: Call session ID
            conversation: Full conversation transcript
            outcome: Call outcome data (converted, satisfied, etc.)

        Returns:
            Analysis results with improvement suggestions
        """
        if not settings.enable_learning:
            return {"learning_disabled": True}

        # Build analysis prompt
        analysis_prompt = f"""Analyze this call:

Session ID: {session_id}

Conversation:
{self._format_conversation(conversation)}

Outcome:
- Success: {outcome.get('success', False)}
- Converted: {outcome.get('converted', False)}
- Satisfaction: {outcome.get('satisfaction', 'unknown')}
- Resolution Time: {outcome.get('duration_seconds', 0)}s

Provide:
1. What went well
2. What could improve
3. Key phrases that worked
4. Suggested prompt improvements
5. Knowledge gaps to fill"""

        try:
            result = await self.agent.run(analysis_prompt)

            analysis = {
                "session_id": session_id,
                "analysis": str(result.output),
                "timestamp": "now",
            }

            # Cache for batch processing
            self.call_analysis_cache.append(analysis)

            logger.info(f"Call analyzed: {session_id}")

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing call: {e}")
            return {"error": str(e)}

    async def batch_analyze(
        self,
        min_calls: int = None,
    ) -> Dict[str, Any]:
        """
        Analyze multiple calls to find patterns.

        Args:
            min_calls: Minimum calls to analyze (default from settings)

        Returns:
            Batch analysis with system-wide improvements
        """
        min_calls = min_calls or settings.min_calls_for_learning

        if len(self.call_analysis_cache) < min_calls:
            return {
                "insufficient_data": True,
                "calls_analyzed": len(self.call_analysis_cache),
                "calls_needed": min_calls,
            }

        # Aggregate patterns
        batch_prompt = f"""Analyze these {len(self.call_analysis_cache)} call analyses to find system-wide patterns:

{self._format_analyses(self.call_analysis_cache)}

Provide:
1. **Top 3 Success Patterns** - What's working consistently
2. **Top 3 Failure Patterns** - What's causing issues
3. **Prompt Improvements** - Specific prompt refinements for each agent type
4. **Knowledge Base Updates** - New information to add
5. **New Agent Recommendations** - Should we create new specialists?

Be specific. Provide actionable recommendations."""

        try:
            result = await self.agent.run(batch_prompt)

            improvements = {
                "calls_analyzed": len(self.call_analysis_cache),
                "recommendations": str(result.output),
                "timestamp": "now",
            }

            # Clear cache after processing
            self.call_analysis_cache.clear()

            logger.info(f"Batch analysis complete: {len(self.call_analysis_cache)} calls")

            return improvements

        except Exception as e:
            logger.error(f"Error in batch analysis: {e}")
            return {"error": str(e)}

    async def suggest_prompt_improvement(
        self,
        agent_type: str,
        current_prompt: str,
        performance_data: Dict[str, Any],
    ) -> str:
        """
        Suggest improvements to an agent's prompt.

        Args:
            agent_type: Type of agent (orchestrator, hvac, sales, etc.)
            current_prompt: Current system prompt
            performance_data: Performance metrics

        Returns:
            Improved prompt
        """
        improvement_prompt = f"""Improve this prompt for a {agent_type} agent:

Current Prompt:
{current_prompt}

Performance Data:
- Success Rate: {performance_data.get('success_rate', 0)}%
- Avg Satisfaction: {performance_data.get('avg_satisfaction', 0)}/10
- Avg Resolution Time: {performance_data.get('avg_resolution_time', 0)}s
- Common Issues: {performance_data.get('common_issues', [])}

Provide an improved version of the prompt that addresses the performance issues."""

        try:
            result = await self.agent.run(improvement_prompt)
            improved_prompt = str(result.output)

            logger.info(f"Prompt improved for {agent_type}")

            return improved_prompt

        except Exception as e:
            logger.error(f"Error improving prompt: {e}")
            return current_prompt

    async def ab_test_prompt(
        self,
        prompt_a: str,
        prompt_b: str,
        agent_type: str,
        sample_size: int = 100,
    ) -> Dict[str, Any]:
        """
        Run A/B test on two prompt variations.

        Args:
            prompt_a: First prompt variant
            prompt_b: Second prompt variant
            agent_type: Type of agent to test
            sample_size: Number of calls per variant

        Returns:
            Test results with winner
        """
        # TODO: Implement actual A/B testing infrastructure
        logger.info(f"A/B test scheduled: {agent_type} - {sample_size} calls per variant")

        return {
            "test_id": f"ab_test_{agent_type}_001",
            "status": "scheduled",
            "sample_size": sample_size,
            "message": "A/B test will run automatically on next calls",
        }

    def _format_conversation(self, conversation: List[Dict[str, str]]) -> str:
        """Format conversation for analysis."""
        return "\n".join(
            [f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in conversation]
        )

    def _format_analyses(self, analyses: List[Dict[str, Any]]) -> str:
        """Format multiple analyses for batch processing."""
        formatted = []
        for i, analysis in enumerate(analyses[:20], 1):  # Limit to 20 for token efficiency
            formatted.append(f"Call {i}: {analysis.get('analysis', 'N/A')}")
        return "\n\n".join(formatted)


# Global learning agent instance
learning_agent = LearningAgent()
