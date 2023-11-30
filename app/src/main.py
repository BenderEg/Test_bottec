import asyncio

from aiogram3_di import DIMiddleware
from redis.asyncio import Redis

from core.bot import get_bot_instance
from core.menu import set_main_menu
from core.config import settings
from db import redis_storage
from handlers import start, subscribe, catalog

async def main() -> None:

    redis_storage.redis = Redis(host=settings.red_host,
                                port=settings.red_port,
                                db=settings.red_db,
                                encoding="utf-8",
                                decode_responses=True)

    bot, dp = await get_bot_instance()

    dp.include_router(start.router)
    dp.include_router(subscribe.router)
    dp.include_router(catalog.router)
    dp.message.middleware(DIMiddleware())
    dp.callback_query.middleware(DIMiddleware())

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
