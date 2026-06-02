from enum import Enum


class ConfigTypeEnum(Enum):
    FORUM = "forum"
    LOGGING = "logging"
    ECONOMY = "economy"
    LEVELS = "levels"
    CLANS = "clans"
    PRIVATE_CHANNELS = "private_channels"
    MODERATION = "moderation"
    NOTIFICATIONS = "notifications"
    INFOMAKER = "infomakers"
    RULES = "rules"
    PROPOSALS = "proposals"
    ROLE_REQUEST = "role_request"
    MULTIPLERS = "multiplers"
    TICKETS = "tickets"
    ACCESS = "access"


class ConfigMuteTypeEnum(Enum):
    TIMEOUT = "timeout"
    ROLE = "role"


class MessageCountTypeEnum(Enum):
    CHANNEL_ONLY = "channel_only"
    ALL = "all"
