from aiogram import executor

from bot.create_bot import dispatcher
from bot.handlers import way_making_with_bot, way_making_without_bot, admin
from bot.handlers import support
from bot import start_menu_handler


def run_bot():
    admin.registration_of_handlers(dispatcher)
    support.registration_of_handlers(dispatcher)
    start_menu_handler.registration_of_handlers(dispatcher)
    way_making_with_bot.registration_of_handlers(dispatcher)
    way_making_without_bot.registration_of_handlers(dispatcher)
    executor.start_polling(dispatcher, skip_updates=False)


if __name__ == '__main__':
    run_bot()
