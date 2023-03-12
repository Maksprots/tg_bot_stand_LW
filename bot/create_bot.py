import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from loguru import logger

logger.add('testing_log.log', format='{time} {level} {message}',
           level='DEBUG')
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, storage=storage)
