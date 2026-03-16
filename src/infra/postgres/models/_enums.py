from enum import Enum


class MetaConfigAccessTypeEnum(Enum):
    """Enumeration for meta config access types."""

    OTHER = "other"
    LOGGING = "logging"
    ECONOMY = "economy"
    LEVELS = "levels"
    CLANS = "clans"
    PRIVATE_CHANNELS = "private_channels"
    MODERATION = "moderation"
    NOTIFICATIONS = "notifications"
    INFOMAKER = "infomaker"

    @classmethod
    def all_values(cls) -> list[str]:
        """Get all enum values."""
        return [choice.value for choice in cls]

    @classmethod
    def from_choice(cls, choice: str) -> "MetaConfigAccessTypeEnum":
        """Get enum member from choice string."""
        mapping = {
            "clans": cls.CLANS,
            "economy": cls.ECONOMY,
            "levels": cls.LEVELS,
            "logging": cls.LOGGING,
            "moderation": cls.MODERATION,
            "notifications": cls.NOTIFICATIONS,
            "private_channels": cls.PRIVATE_CHANNELS,
            "other": cls.OTHER,
            "infomaker": cls.INFOMAKER,
        }
        return mapping[choice]
