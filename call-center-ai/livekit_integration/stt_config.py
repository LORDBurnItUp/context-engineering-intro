"""STT (Speech-to-Text) configuration and utilities."""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class STTProvider(str, Enum):
    """Supported STT providers."""

    OPENAI = "openai"  # Whisper API
    DEEPGRAM = "deepgram"


class STTModel(str, Enum):
    """STT model options."""

    # OpenAI models
    WHISPER_1 = "whisper-1"

    # Deepgram models
    NOVA_2 = "nova-2"  # Latest, most accurate
    NOVA_2_GENERAL = "nova-2-general"
    NOVA_2_PHONECALL = "nova-2-phonecall"  # Optimized for phone calls
    NOVA_2_MEETING = "nova-2-meeting"
    ENHANCED = "enhanced"  # Legacy, still accurate


@dataclass
class STTConfig:
    """Configuration for STT provider."""

    provider: STTProvider
    model: str
    language: str = "en-US"
    punctuate: bool = True
    interim_results: bool = True  # Real-time partial results
    endpointing: Optional[int] = None  # Milliseconds of silence to end utterance

    @classmethod
    def openai_default(cls) -> "STTConfig":
        """
        Get default OpenAI Whisper configuration.

        Returns:
            OpenAI STT config
        """
        return cls(
            provider=STTProvider.OPENAI,
            model=STTModel.WHISPER_1.value,
            language="en",
            punctuate=True,
        )

    @classmethod
    def deepgram_fast(cls) -> "STTConfig":
        """
        Get fast Deepgram configuration (phone call optimized).

        Returns:
            Deepgram STT config optimized for speed
        """
        return cls(
            provider=STTProvider.DEEPGRAM,
            model=STTModel.NOVA_2_PHONECALL.value,
            language="en-US",
            punctuate=True,
            interim_results=True,
            endpointing=300,  # 300ms silence ends utterance
        )

    @classmethod
    def deepgram_accurate(cls) -> "STTConfig":
        """
        Get accurate Deepgram configuration.

        Returns:
            Deepgram STT config optimized for accuracy
        """
        return cls(
            provider=STTProvider.DEEPGRAM,
            model=STTModel.NOVA_2.value,
            language="en-US",
            punctuate=True,
            interim_results=True,
            endpointing=500,  # Longer silence for better accuracy
        )

    @classmethod
    def for_use_case(cls, use_case: str, use_premium: bool = True) -> "STTConfig":
        """
        Get STT config optimized for a specific use case.

        Args:
            use_case: Use case type (phone, meeting, general)
            use_premium: Whether to use premium provider (Deepgram)

        Returns:
            Optimized STT config
        """
        if not use_premium:
            return cls.openai_default()

        if use_case == "phone":
            return cls.deepgram_fast()
        elif use_case == "meeting":
            return cls(
                provider=STTProvider.DEEPGRAM,
                model=STTModel.NOVA_2_MEETING.value,
                language="en-US",
                punctuate=True,
                interim_results=True,
            )
        else:
            return cls.deepgram_accurate()


def get_recommended_stt(
    call_type: str = "phone",
    need_speed: bool = True,
) -> STTConfig:
    """
    Get recommended STT configuration.

    Args:
        call_type: Type of call (phone, meeting, general)
        need_speed: Whether to prioritize speed over accuracy

    Returns:
        Recommended STT configuration
    """
    if need_speed:
        # Fast STT for real-time conversations
        return STTConfig.deepgram_fast()
    else:
        # Accurate STT for important calls
        return STTConfig.deepgram_accurate()
