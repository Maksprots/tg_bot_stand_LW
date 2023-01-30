from aiogram import executor
from create_bot import dispatcher
from handlers import way_making_with_bot, way_making_without_bot
from handlers import support_implementation
from bot import start_menu_handler


support_implementation.registration_of_handlers(dispatcher)
start_menu_handler.registration_of_handlers(dispatcher)
way_making_with_bot.registration_of_handlers(dispatcher)
way_making_without_bot.registration_of_handlers(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=False)
