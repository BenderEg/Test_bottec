from typing import Annotated

from aiogram3_di import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from db.redis_storage import get_redis
from services.user_service import UserService
from services.product_service import ProductService

db_session = Annotated[AsyncSession, Depends(get_session)]
redis_client = Annotated[Redis, Depends(get_redis)]

async def get_user_service(db: db_session) -> UserService:
    return UserService(db)

async def get_product_service(db: db_session) -> ProductService:
    return ProductService(db)

user_service = Annotated[UserService, Depends(get_user_service)]
product_service = Annotated[ProductService, Depends(get_product_service)]