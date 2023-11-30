from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/catalog',
                   description='Категории товаров'),
        BotCommand(command='/subcategories',
                   description='Подкатегории товаров'),
        BotCommand(command='/items',
                   description='Товары'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/cancel',
                   description='Для выхода из режима'),
            ]
    await bot.set_my_commands(main_menu_commands)