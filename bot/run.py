from aiogram import executor
from create_bot import dispatcher

from handlers import MainMenuw12, way1, way2

MainMenuw12.register_handlers_MainMenuw12(dispatcher)
way1.register_handlers_way1(dispatcher)
way2.register_handlers_way2(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=False)
