from json import dumps, loads

from redis.asyncio import Redis
from sqlalchemy import select

from core.config import settings
from db.shemas import Question
from services.base_service import BaseService


class FAQService(BaseService):

    async def get_faq(self) -> list:
        query = select(
            Question.question, Question.answer
            ).where(Question.status == True).order_by(
                Question.question)
        result = await self.db.execute(query)
        faq_list = [(ele[0].lower(), ele[1]) for ele in result.all()]
        return faq_list

    async def put_faq_to_cache(self, name: str,
                               faq_list: list,
                               client: Redis) -> None:
        await client.set(name=name, value=dumps(faq_list),
                         ex=settings.cache_exp)

    async def get_faq_from_cache(self, name: str,
                                 client: Redis) -> list:
        faq_list = await client.get(name=name)
        if faq_list:
            return loads(faq_list)

    def filter_faq_list(self, faq_list: str,
                        target: str) -> list:
        result = list(filter(lambda x: x[0].find(target) != -1, faq_list))
        return result