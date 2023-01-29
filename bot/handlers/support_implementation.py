from aiogram import Dispatcher, types
from bot.create_bot import bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot import markups as mp
import yaml
import os

TEXT_PATH = '/static/texts/answers_text_with_bot.yaml'
LANGUAGE = 'RU'

with open(os.getcwd() + TEXT_PATH,
          encoding='UTF-8') as f:
    read_answers = yaml.safe_load(f)

class ClientStatesGroup(StatesGroup):
    nothing = State()

async def support_anwser(message: types.Message) -> None:
    await message.answer(read_answers[LANGUAGE]['support_greetings'],
                         reply_markup=mp.support)

async def send_appeal(message: types.Message):
    if message.text is None:
        pass
    else:
        await message.forward(-1001859110427, message.text)
        if message.is_forward == 0:
            await message.answer(read_answers[LANGUAGE]['call_not_successful'],
                         reply_markup=mp.send)
        else:
            await message.answer(read_answers[LANGUAGE]['call_successful'],
                         reply_markup=mp.send)

def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        support_anwser, commands=["Поддержка"],  state="*")
    dispatcher.register_message_handler(
        send_appeal, Text(equals="Отправить", ignore_case=True),  state="*")
