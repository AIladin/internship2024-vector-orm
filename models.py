from typing import Optional

import inflection
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy import orm


class CommonMixin:
    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        return inflection.underscore(cls.__name__)

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)


class Base(orm.DeclarativeBase):
    pass


class Game(Base, CommonMixin):
    name: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    samples: orm.Mapped[list["Sample"]] = orm.relationship(back_populates="game")
    clusters: orm.Mapped[list["Cluster"]] = orm.relationship(back_populates="game")


class Cluster(Base, CommonMixin):
    game_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Game.id))

    game: orm.Mapped[Game] = orm.relationship(back_populates="clusters")
    samples: orm.Mapped[list["Sample"]] = orm.relationship(back_populates="cluster")


class Sample(Base, CommonMixin):
    game_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Game.id))

    game: orm.Mapped[Game] = orm.relationship(back_populates="samples")

    cluster_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey(Cluster.id), nullable=True, server_default=None
    )

    cluster: orm.Mapped[Optional[Cluster]] = orm.relationship(back_populates="samples")

    s3_path: orm.Mapped[str] = orm.mapped_column(sa.String(512))
    embedding: orm.Mapped[list[float]] = orm.mapped_column(Vector(), nullable=True)
    thumbnail_path: orm.Mapped[str] = orm.mapped_column(sa.String(512), nullable=True)
