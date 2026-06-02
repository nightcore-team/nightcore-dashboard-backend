from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.postgres.models._mixins import IdIntegerMixin
from src.infra.postgres.models.base import Base


class GuildProposalsConfig(IdIntegerMixin, Base):
    guild_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    create_proposal_channel_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    proposals_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
