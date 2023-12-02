from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

from core.dependencies import faq_service, redis_client
from core.logger import logging

router: Router = Router()

@router.inline_query()
async def process_faq(query: InlineQuery,
                      service: faq_service,
                      red_client: redis_client):
    try:
        questions = await service.get_faq_from_cache('faq', red_client)
        if not questions:
            questions = await service.get_faq()
            await service.put_faq_to_cache('faq', questions, red_client)
        if questions:
            results = service.filter_faq_list(questions, query.query.lower())
            query_result = []
            for i, ele in enumerate(results, 1):
                query_result.append(InlineQueryResultArticle(
                    id=f'id {i}',
                    title=f'{ele[0]}',
                    description=f'{ele[1]}',
                    input_message_content=InputTextMessageContent(
                        message_text=f'{ele[1]}',
                    )
                ))
            await query.answer(query_result, is_personal=True)
    except Exception as err:
        logging.error(err)