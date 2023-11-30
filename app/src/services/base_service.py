from sqlalchemy.ext.asyncio import AsyncSession

from db.shemas import User

class BaseService():

    def __init__(self, db: AsyncSession) -> None:

        self.db = db

    async def get_user_by_id(self, id: int) -> User:
        user = await self.db.get(User, id)
        return user