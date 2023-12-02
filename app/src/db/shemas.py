import uuid

from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

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

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return f'User {self.name}'


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
        return f'Category {self.name}'


class SubCategory(Base):
    __tablename__ = 'subcategory'

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(
        'category.id', ondelete='CASCADE'))
    created: Mapped[timestamp]
    modified: Mapped[timestamp_upd]

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f'Subcategory {self.name}'


class Item(Base):
    __tablename__ = 'item'

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    image_path: Mapped[str]
    subcategory_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(
        'category.id', ondelete='CASCADE'))
    created: Mapped[timestamp]
    modified: Mapped[timestamp_upd]

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f'Item {self.name}'


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[uuid_pk]
    client_id: Mapped[int]
    address: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)
    created: Mapped[timestamp]

    def __init__(self, client_id: int,
                 address: str):
        self.client_id = client_id
        self.address = address

    def __str__(self) -> str:
        return f'Order {self.id} from {self.client_id}'


class OrderItems(Base):
    __tablename__ = 'order_item'

    id: Mapped[uuid_pk]
    order_id: Mapped[uuid.UUID]
    item_id: Mapped[uuid.UUID]
    quantity: Mapped[int]
    created: Mapped[timestamp]
    modified: Mapped[timestamp_upd]

    def __init__(self, order_id: uuid.UUID,
                 item_id: uuid.UUID,
                 quantity: int):
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity

    def __str__(self) -> str:
        return f'Order details {self.id}'


class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[uuid_pk]
    question: Mapped[str]
    answer: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)
    created: Mapped[timestamp]
    modified: Mapped[timestamp_upd]

    def __init__(self, question: str):
        self.question = question

    def __str__(self) -> str:
        return f'{self.question}'