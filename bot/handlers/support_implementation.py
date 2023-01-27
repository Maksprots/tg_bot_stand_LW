from aiogram import Dispatcher, types
from bot.create_bot import bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot import markups as mp
import yaml
import os

TEXT_PATH = '/static/texts/answers_text_with_bot.yaml'

with open(os.getcwd() + TEXT_PATH,
          encoding='UTF-8') as f:
    read_answers = yaml.safe_load(f)

async def support_anwser(message: types.Message) -> None:
    await message.answer(read_answers['RU']['chosen_way_with_bot_2'],
                         reply_markup=mp.support)


def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        support_anwser, commands=["Поддержка"], state="*")