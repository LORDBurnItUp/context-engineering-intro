"""LiveKit Voice Agent wrapper for real-time conversations."""

import asyncio
from typing import Optional, Callable, Any
from dataclasses import dataclass

from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, deepgram, elevenlabs, silero

from config import settings
from loguru import logger


@dataclass
class VoiceAgentConfig:
    """Configuration for voice agent."""

    agent_id: str
    industry: str  # hvac, roofing, solar
    role: str  # support, troubleshoot, sales, cold_call
    voice_id: Optional[str] = None  # For ElevenLabs
    use_premium_tts: bool = False
    use_fast_stt: bool = True
    enable_interruptions: bool = True


class VoiceAgent:
    """
    Wrapper for LiveKit voice agent with multi-provider support.

    Handles real-time voice conversations with automatic STT/TTS,
    intelligent agent routing, and conversation management.
    """

    def __init__(
        self,
        config: VoiceAgentConfig,
        llm_callback: Callable[[str, dict], str],
    ):
        """
        Initialize voice agent.

        Args:
            config: Voice agent configuration
            llm_callback: Async function to call for LLM responses
        """
        self.config = config
        self.llm_callback = llm_callback
        self.session_id: Optional[str] = None
        self.conversation_history: list[dict] = []

        # Initialize providers
        self._setup_providers()

        logger.info(
            f"VoiceAgent initialized: {config.agent_id} "
            f"(Industry: {config.industry}, Role: {config.role})"
        )

    def _setup_providers(self):
        """Set up TTS and STT providers based on configuration."""

        # TTS Provider Selection
        if self.config.use_premium_tts and settings.elevenlabs_api_key:
            self.tts = elevenlabs.TTS(
                api_key=settings.elevenlabs_api_key,
                voice_id=self.config.voice_id or "pNInz6obpgDQGcFmaJgB",  # Adam voice
                model_id="eleven_turbo_v2_5",
            )
            logger.info("Using ElevenLabs TTS (premium)")
        else:
            self.tts = openai.TTS(
                api_key=settings.openai_api_key,
                model="tts-1",
                voice="alloy",
            )
            logger.info("Using OpenAI TTS")

        # STT Provider Selection
        if self.config.use_fast_stt and settings.deepgram_api_key:
            self.stt = deepgram.STT(
                api_key=settings.deepgram_api_key,
                model="nova-2",
                language="en-US",
            )
            logger.info("Using Deepgram STT (fast)")
        else:
            self.stt = openai.STT(
                api_key=settings.openai_api_key,
                model="whisper-1",
            )
            logger.info("Using OpenAI Whisper STT")

        # Voice Activity Detection
        self.vad = silero.VAD.load()

    async def start_conversation(
        self,
        room: rtc.Room,
        participant: rtc.Participant,
    ) -> VoiceAssistant:
        """
        Start a voice conversation with a participant.

        Args:
            room: LiveKit room
            participant: Remote participant

        Returns:
            VoiceAssistant instance
        """
        self.session_id = f"{self.config.agent_id}_{room.name}"

        logger.info(
            f"Starting conversation: {self.session_id} "
            f"with participant {participant.identity}"
        )

        # Create the voice assistant
        assistant = VoiceAssistant(
            vad=self.vad,
            stt=self.stt,
            llm=self._create_llm_wrapper(),
            tts=self.tts,
            chat_ctx=self._get_initial_chat_context(),
            allow_interruptions=self.config.enable_interruptions,
        )

        # Start the assistant
        assistant.start(room, participant)

        logger.info(f"Voice assistant started: {self.session_id}")
        return assistant

    def _create_llm_wrapper(self) -> llm.LLM:
        """
        Create LLM wrapper that integrates with our agent system.

        Returns:
            LLM instance configured for the agent
        """
        # Use OpenAI-compatible wrapper but route to our agent callback
        # This allows us to use any LLM backend (Anthropic, OpenAI, etc.)

        llm_instance = openai.LLM(
            model="gpt-4",  # We'll override this with our callback
            api_key=settings.openai_api_key,
        )

        # Wrap the LLM to route through our agent system
        return self._wrap_llm_with_agent(llm_instance)

    def _wrap_llm_with_agent(self, base_llm: llm.LLM) -> llm.LLM:
        """
        Wrap the base LLM to route requests through our agent system.

        This allows us to use our orchestrator and specialized agents
        while maintaining LiveKit's VoiceAssistant interface.

        Args:
            base_llm: Base LLM instance

        Returns:
            Wrapped LLM that routes through our agents
        """
        # For now, return base LLM - we'll enhance this to route through orchestrator
        # TODO: Implement agent routing in the LLM wrapper
        return base_llm

    def _get_initial_chat_context(self) -> llm.ChatContext:
        """
        Get initial chat context with system prompt.

        Returns:
            Initial chat context for the conversation
        """
        # Load the appropriate prompt based on industry and role
        system_prompt = self._load_system_prompt()

        return llm.ChatContext(
            messages=[
                llm.ChatMessage(
                    role="system",
                    content=system_prompt,
                )
            ]
        )

    def _load_system_prompt(self) -> str:
        """
        Load system prompt for the agent's industry and role.

        Returns:
            System prompt string
        """
        # Default prompt - will be replaced by orchestrator routing
        base_prompt = f"""You are an AI assistant specializing in {self.config.industry}
for {self.config.role} inquiries. You are professional, knowledgeable, and helpful.

Your goal is to provide excellent customer service and help resolve any issues or questions
the customer may have. You speak naturally and conversationally.

If you need to transfer the call to a specialist, say "Let me transfer you to someone
who can better help with that."""

        return base_prompt

    async def end_conversation(self):
        """End the conversation and cleanup resources."""
        logger.info(f"Ending conversation: {self.session_id}")

        # Store conversation for learning
        if settings.enable_learning and len(self.conversation_history) > 0:
            await self._store_conversation_for_learning()

        self.conversation_history.clear()

    async def _store_conversation_for_learning(self):
        """Store conversation history for the learning agent."""
        # TODO: Implement conversation storage for self-improvement
        logger.info(
            f"Storing conversation for learning: {len(self.conversation_history)} turns"
        )


async def entrypoint(ctx: JobContext):
    """
    Main entry point for LiveKit job.

    This is called when a participant joins a room.
    """
    logger.info(f"Connecting to room: {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant
    participant = await ctx.wait_for_participant()
    logger.info(f"Participant joined: {participant.identity}")

    # Create voice agent with default config
    # In production, this would be determined by the room metadata
    config = VoiceAgentConfig(
        agent_id=f"agent_{ctx.room.name}",
        industry=settings.default_industry,
        role=settings.default_role,
        use_premium_tts=False,  # Start with basic, upgrade if needed
        use_fast_stt=True,
    )

    # Create dummy callback for now - will integrate with orchestrator
    async def dummy_llm_callback(user_input: str, context: dict) -> str:
        """Temporary callback until orchestrator is integrated."""
        return f"I received your message: {user_input}"

    agent = VoiceAgent(config=config, llm_callback=dummy_llm_callback)

    # Start the conversation
    assistant = await agent.start_conversation(ctx.room, participant)

    # Wait for conversation to end
    await assistant.wait_until_done()

    # Cleanup
    await agent.end_conversation()
    logger.info(f"Conversation ended: {agent.session_id}")


if __name__ == "__main__":
    """Run the voice agent worker."""
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            api_key=settings.livekit_api_key,
            api_secret=settings.livekit_api_secret,
            ws_url=settings.livekit_url,
        ),
    )
