"""Guild model for the Nightcore bot database."""

from sqlalchemy import ARRAY, JSON, BigInteger, Float, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.postgres.models._annot import (
    Rules,
)
from src.infra.postgres.models._mixins import IdIntegerMixin
from src.infra.postgres.models._types import (
    DiscordCategoryID,
    DiscordChannelID,
    DiscordRoleID,
)
from src.infra.postgres.models.base import Base


class GuildOrgRolesConfig(IdIntegerMixin, Base):
    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    illegal_roles: Mapped[dict[str, dict[str, int]]] = mapped_column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    organizational_roles: Mapped[dict[str, dict[str, int]]] = mapped_column(
        JSON, nullable=False, default=dict
    )
    check_role_requests_channel_id: Mapped[DiscordChannelID | None] = (
        mapped_column(BigInteger, nullable=True)
    )


class GuildRulesConfig(IdIntegerMixin, Base):
    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    guild_rules: Mapped["Rules"] = mapped_column(
        JSON,
        nullable=False,
        default=lambda: {"chapters": []},  # type: ignore
        server_default=text("'{\"chapters\": []}'::json"),
    )
    rules_channel_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )


class GuildProposalConfig(IdIntegerMixin, Base):
    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    create_proposal_channel_id: Mapped[DiscordChannelID | None] = (
        mapped_column(BigInteger, nullable=True)
    )
    proposals_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )


class GuildLoggingConfig(IdIntegerMixin, Base):  #
    """Logging configuration for a guild."""

    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    bans_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    clans_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    members_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    messages_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    voices_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    moderation_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    tickets_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    roles_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    channels_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    reactions_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    private_rooms_log_channel_id: Mapped[DiscordChannelID | None] = (
        mapped_column(BigInteger, nullable=True)
    )
    economy_log_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    message_log_ignoring_channels_ids: Mapped[
        list[DiscordChannelID] | None
    ] = mapped_column(ARRAY(BigInteger), nullable=True)


class GuildEconomyConfig(IdIntegerMixin, Base):  #
    """Economy configuration for a guild."""

    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )

    coin_name: Mapped[str | None] = mapped_column(String, nullable=True)
    economy_access_roles_ids: Mapped[list[DiscordChannelID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )
    reward_bonus: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    economy_shop_buy_ping_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )
    economy_shop_items: Mapped[dict[str, int]] = mapped_column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    casino_multiplayer_channel_id: Mapped[DiscordChannelID | None] = (
        mapped_column(BigInteger, nullable=True)
    )
    color_drop_compensation: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )


class GuildLevelsConfig(IdIntegerMixin, Base):  #
    """Level configuration for a guild."""

    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )

    count_messages_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    level_notify_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    bonus_access_roles_ids: Mapped[dict[int, int]] = mapped_column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    level_roles: Mapped[dict[str, int]] = mapped_column(
        JSON, nullable=False, default=dict, server_default=text("'{}'::json")
    )
    count_messages_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="channel_only",
        server_default=text("'channel_only'"),
    )  # all | channel_only


class GuildMultiplersConfig(IdIntegerMixin, Base):
    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    base_exp_multiplier: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )
    temp_exp_multiplier: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    base_coins_multiplier: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )
    temp_coins_multiplier: Mapped[int | None] = mapped_column(
        Float, nullable=True
    )
    base_battlepass_multiplier: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default=text("1")
    )
    temp_battlepass_multiplier: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )


class GuildClansConfig(IdIntegerMixin, Base):
    """Clans configuration for a guild."""

    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    create_clan_channel_category_id: Mapped[DiscordCategoryID | None] = (
        mapped_column(BigInteger, nullable=True)
    )
    clan_payday_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    clan_shop_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    clan_shop_items: Mapped[dict[str, int]] = mapped_column(
        JSON, nullable=False, default=dict
    )
    clans_access_roles_ids: Mapped[list[DiscordRoleID] | None] = mapped_column(
        ARRAY(BigInteger), nullable=True
    )
    clan_buy_ping_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )
    clan_reputation_per_payday: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default=text("1")
    )
    base_exp_multiplier: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default=text("1")
    )
    clan_improvements: Mapped[list[int]] = mapped_column(
        ARRAY(Integer), nullable=False, default=list
    )


class GuildPrivateChannelsConfig(IdIntegerMixin, Base):
    """Private channels configuration for a guild."""

    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    private_rooms_create_channel_id: Mapped[DiscordChannelID | None] = (
        mapped_column(BigInteger, nullable=True)
    )


class GuildModerationConfig(IdIntegerMixin, Base):  #
    """Moderation configuration for a guild."""

    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    moderation_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )  #
    leadership_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )  #
    count_moderator_messages_channel_id: Mapped[DiscordChannelID | None] = (
        mapped_column(BigInteger, nullable=True)
    )  #
    ban_access_roles_ids: Mapped[list[DiscordRoleID] | None] = mapped_column(
        ARRAY(BigInteger), nullable=True
    )  #
    unban_access_roles_ids: Mapped[list[DiscordRoleID] | None] = mapped_column(
        ARRAY(BigInteger), nullable=True
    )
    mute_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )  #
    ban_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )  #
    kick_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )  #
    ticket_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )  #
    role_request_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )
    role_remove_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )
    ticket_ban_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )
    mpmute_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )
    vmute_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )
    message_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )
    notification_score: Mapped[float | None] = mapped_column(
        Float, nullable=False, default=0.0, server_default=text("0.0")
    )

    trackable_moderation_role_id: Mapped[DiscordRoleID | None] = mapped_column(
        BigInteger, nullable=True
    )  #

    ban_request_ping_role_id: Mapped[DiscordRoleID | None] = mapped_column(
        BigInteger, nullable=True
    )  #
    send_ban_request_channel_id: Mapped[DiscordChannelID | None] = (
        mapped_column(BigInteger, nullable=True)
    )  #
    mpmute_role_id: Mapped[DiscordRoleID | None] = mapped_column(
        BigInteger, nullable=True
    )  #
    vmute_role_id: Mapped[DiscordRoleID | None] = mapped_column(
        BigInteger, nullable=True
    )  ##
    mute_role_id: Mapped[DiscordRoleID | None] = mapped_column(
        BigInteger, nullable=True
    )
    mute_type: Mapped[str] = mapped_column(
        String, nullable=False, default="role"
    )  #
    fraction_roles_access_roles_ids: Mapped[dict[str, list[DiscordRoleID]]] = (
        mapped_column(JSON, nullable=False, default=dict)
    )  #
    leader_access_rr_roles_ids: Mapped[list[DiscordRoleID]] = mapped_column(
        ARRAY(BigInteger), nullable=False, default=list
    )  #


class GuildNotificationsConfig(IdIntegerMixin, Base):  #
    """Notifications configuration for a guild."""

    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    notifications_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    notifications_for_moderation_channel_id: Mapped[
        DiscordChannelID | None
    ] = mapped_column(BigInteger, nullable=True)
    notifications_from_bot_channel_id: Mapped[DiscordChannelID] = (
        mapped_column(BigInteger, nullable=True)
    )


class GuildTicketsConfig(IdIntegerMixin, Base):
    """Tickets configuration for a guild."""

    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    tickets_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    new_tickets_category_id: Mapped[DiscordCategoryID | None] = mapped_column(
        BigInteger, nullable=True
    )
    closed_tickets_category_id: Mapped[DiscordCategoryID | None] = (
        mapped_column(BigInteger, nullable=True)
    )
    create_ticket_channel_id: Mapped[DiscordChannelID | None] = mapped_column(
        BigInteger, nullable=True
    )
    pinned_tickets_category_id: Mapped[DiscordCategoryID | None] = (
        mapped_column(BigInteger, nullable=True)
    )
    create_ticket_ping_role_id: Mapped[DiscordRoleID | None] = mapped_column(
        BigInteger, nullable=True
    )


class GuildInfomakerConfig(IdIntegerMixin, Base):
    """Infomaker configuration for a guild."""

    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    admins_roles_ids: Mapped[list[DiscordRoleID] | None] = mapped_column(
        ARRAY(BigInteger), nullable=True
    )
    leaders_roles_ids: Mapped[list[DiscordRoleID] | None] = mapped_column(
        ARRAY(BigInteger), nullable=True
    )
    admins_roles_logging_channel_id: Mapped[DiscordChannelID | None] = (
        mapped_column(BigInteger, nullable=True)
    )
    leaders_roles_logging_channel_id: Mapped[DiscordRoleID | None] = (
        mapped_column(BigInteger, nullable=True)
    )


class GuildForumConfig(IdIntegerMixin, Base):
    """Forum configuration for a guild."""

    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    section_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True
    )
    channel_id: Mapped[DiscordChannelID] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    role_id: Mapped[DiscordRoleID] = mapped_column(
        BigInteger, nullable=False, unique=True
    )


class GuildAccessConfig(IdIntegerMixin, Base):
    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )

    # Access to GuildFaqConfig
    faq_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildForumConfig
    forum_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildOrgRolesConfig
    org_roles_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildProposalConfig
    proposal_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildRulesConfig
    rules_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildMultiplersConfig
    multiplers_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildLoggingConfig
    logging_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildEconomyConfig
    economy_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildLevelsConfig
    levels_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildClansConfig
    clans_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildPrivateChannelsConfig
    private_channels_config_access_roles_ids: Mapped[
        list[DiscordRoleID] | None
    ] = mapped_column(ARRAY(BigInteger), nullable=True)

    # Access to GuildModerationConfig
    moderation_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildNotificationsConfig
    notifications_config_access_roles_ids: Mapped[
        list[DiscordRoleID] | None
    ] = mapped_column(ARRAY(BigInteger), nullable=True)

    # Access to GuildTicketsConfig
    tickets_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )

    # Access to GuildInfomakerConfig
    infomaker_config_access_roles_ids: Mapped[list[DiscordRoleID] | None] = (
        mapped_column(ARRAY(BigInteger), nullable=True)
    )
