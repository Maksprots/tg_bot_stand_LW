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

class ClientStatesGroup2(StatesGroup):
    nothing = State()
    board = State()
    desc = State()

async def support_anwser(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(read_answers['RU']['chosen_way_with_bot_2'],
                         reply_markup=mp.write_messege)


def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        support_anwser, Text(equals=read_answers['RU']['to_first_method'],
                          ignore_case=True), state="*")
