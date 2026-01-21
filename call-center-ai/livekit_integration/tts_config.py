"""TTS (Text-to-Speech) configuration and utilities."""

from enum import Enum
from typing import Optional
from dataclasses import dataclass


class TTSProvider(str, Enum):
    """Supported TTS providers."""

    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"


class VoiceProfile(str, Enum):
    """Pre-configured voice profiles for different use cases."""

    # ElevenLabs voices
    PROFESSIONAL_MALE = "pNInz6obpgDQGcFmaJgB"  # Adam
    PROFESSIONAL_FEMALE = "EXAVITQu4vr4xnSDxMaL"  # Sarah
    FRIENDLY_MALE = "VR6AewLTigWG4xSOukaG"  # Arnold
    FRIENDLY_FEMALE = "jsCqWAovK2LkecY7zXl4"  # Freya

    # OpenAI voices
    OPENAI_ALLOY = "alloy"  # Neutral
    OPENAI_ECHO = "echo"  # Male
    OPENAI_FABLE = "fable"  # British male
    OPENAI_ONYX = "onyx"  # Deep male
    OPENAI_NOVA = "nova"  # Female
    OPENAI_SHIMMER = "shimmer"  # Soft female


@dataclass
class TTSConfig:
    """Configuration for TTS provider."""

    provider: TTSProvider
    voice_id: str
    model: Optional[str] = None
    speed: float = 1.0
    stability: float = 0.5  # ElevenLabs only
    similarity_boost: float = 0.75  # ElevenLabs only

    @classmethod
    def openai_default(cls) -> "TTSConfig":
        """
        Get default OpenAI TTS configuration.

        Returns:
            OpenAI TTS config with neutral voice
        """
        return cls(
            provider=TTSProvider.OPENAI,
            voice_id=VoiceProfile.OPENAI_ALLOY.value,
            model="tts-1",
            speed=1.0,
        )

    @classmethod
    def openai_fast(cls) -> "TTSConfig":
        """
        Get fast OpenAI TTS configuration (HD quality).

        Returns:
            OpenAI TTS config optimized for speed
        """
        return cls(
            provider=TTSProvider.OPENAI,
            voice_id=VoiceProfile.OPENAI_NOVA.value,
            model="tts-1-hd",
            speed=1.1,
        )

    @classmethod
    def elevenlabs_premium(cls, voice_profile: VoiceProfile = VoiceProfile.PROFESSIONAL_FEMALE) -> "TTSConfig":
        """
        Get premium ElevenLabs TTS configuration.

        Args:
            voice_profile: Voice profile to use

        Returns:
            ElevenLabs TTS config with premium voice
        """
        return cls(
            provider=TTSProvider.ELEVENLABS,
            voice_id=voice_profile.value,
            model="eleven_turbo_v2_5",
            speed=1.0,
            stability=0.5,
            similarity_boost=0.75,
        )

    @classmethod
    def for_role(cls, role: str, use_premium: bool = False) -> "TTSConfig":
        """
        Get TTS config optimized for a specific role.

        Args:
            role: Agent role (support, sales, etc.)
            use_premium: Whether to use premium voices

        Returns:
            Optimized TTS config for the role
        """
        if not use_premium:
            # Use OpenAI for cost efficiency
            if role in ["support", "troubleshoot"]:
                return cls.openai_default()
            elif role in ["sales", "cold_call"]:
                return cls(
                    provider=TTSProvider.OPENAI,
                    voice_id=VoiceProfile.OPENAI_NOVA.value,  # Warmer voice for sales
                    model="tts-1",
                    speed=1.0,
                )
            else:
                return cls.openai_default()
        else:
            # Use ElevenLabs premium
            if role in ["support", "troubleshoot"]:
                return cls.elevenlabs_premium(VoiceProfile.PROFESSIONAL_FEMALE)
            elif role in ["sales", "cold_call"]:
                return cls.elevenlabs_premium(VoiceProfile.FRIENDLY_FEMALE)
            else:
                return cls.elevenlabs_premium()


def get_recommended_voice(
    industry: str,
    role: str,
    gender_preference: Optional[str] = None,
) -> VoiceProfile:
    """
    Get recommended voice profile based on industry, role, and preferences.

    Args:
        industry: Industry context
        role: Agent role
        gender_preference: Optional gender preference ("male" or "female")

    Returns:
        Recommended voice profile
    """
    # Sales and cold calling benefit from warm, friendly voices
    if role in ["sales", "cold_call"]:
        if gender_preference == "male":
            return VoiceProfile.FRIENDLY_MALE
        return VoiceProfile.FRIENDLY_FEMALE

    # Support and troubleshooting benefit from professional voices
    elif role in ["support", "troubleshoot"]:
        if gender_preference == "male":
            return VoiceProfile.PROFESSIONAL_MALE
        return VoiceProfile.PROFESSIONAL_FEMALE

    # Default to professional female
    return VoiceProfile.PROFESSIONAL_FEMALE
