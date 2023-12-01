from typing import Annotated

from aiogram3_di import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from db.redis_storage import get_redis
from services.bucket_service import BucketService
from services.product_service import ProductService
from services.user_service import UserService


db_session = Annotated[AsyncSession, Depends(get_session)]
redis_client = Annotated[Redis, Depends(get_redis)]

async def get_user_service(db: db_session) -> UserService:
    return UserService(db)

async def get_product_service(db: db_session) -> ProductService:
    return ProductService(db)

async def get_bucket_service(db: db_session) -> BucketService:
    return BucketService(db)

user_service = Annotated[UserService, Depends(get_user_service)]
product_service = Annotated[ProductService, Depends(get_product_service)]
bucket_service = Annotated[BucketService, Depends(get_bucket_service)]