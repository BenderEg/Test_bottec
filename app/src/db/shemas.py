import uuid

from datetime import datetime, date
from typing import Annotated

from sqlalchemy import String, ForeignKey, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql import expression

from db.postgres import Base

uuid_pk = Annotated[uuid.UUID, mapped_column(
    primary_key=True,
    default=uuid.uuid4)]

timestamp = Annotated[datetime,
mapped_column(TIMESTAMP(timezone=True),
              default=datetime.utcnow,
              nullable=False)]

timestamp_upd = Annotated[datetime,
mapped_column(TIMESTAMP(timezone=True),
              onupdate=datetime.utcnow,
              default=datetime.utcnow,
              nullable=False)]

class User(Base):
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    group_subscription: Mapped[bool] = mapped_column(default=False)
    channel_subscription: Mapped[bool] = mapped_column(default=False)
    created: Mapped[timestamp]
    modified: Mapped[timestamp_upd]

    #objects: Mapped[list['Object']] = relationship(lazy='selectin')
    #categories: Mapped[list['Category']] = relationship(lazy='selectin')

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return f'<User {self.name}>'


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    created: Mapped[timestamp]
    modified: Mapped[timestamp_upd]

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f'<Category {self.name}>'