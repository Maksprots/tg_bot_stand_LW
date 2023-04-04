import yaml
import os
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from dotenv import load_dotenv

from bot.create_bot import bot
from bot import markups as mp
from bot.config import TEXT_PATH_WITH

# todo перенести в глобал конфиг
load_dotenv()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

LANGUAGE = 'RU'
# TODO придумать что-то чтобы все открытия файлов прозодили в одном месте а не в трех
with open(TEXT_PATH_WITH,
          encoding='UTF-8') as f:
    read_answers = yaml.safe_load(f)


# todo перенести все состояния в отдельный файл
class UserState(StatesGroup):
    name = State()
    email = State()
    ticket = State()


async def support_answer(message: types.Message):
    await message.answer(read_answers[LANGUAGE]['support_greetings'],
                         reply_markup=mp.support)
    await message.answer(read_answers[LANGUAGE]['write_name'])
    await UserState.name.set()


async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer(read_answers[LANGUAGE]['write_email'])
    await UserState.next()


async def get_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer(read_answers[LANGUAGE]['write_warning'])
    await UserState.next()


async def get_ticket(message: types.Message, state: FSMContext):
    await state.update_data(ticket=message.text)
    data = await state.get_data()
    print(data)

    await message.answer(read_answers[LANGUAGE]['string_name']
                         + f": {data['username']}\n")
    await message.answer(read_answers[LANGUAGE]['string_email']
                         + f": {data['email']}\n")
    await message.answer(read_answers[LANGUAGE]['string_ticket']
                         + f": {data['ticket']}")
    await bot.send_message(CHAT_ID, read_answers[LANGUAGE]['string_name']
                           + f": {data['username']}\n")
    await bot.send_message(CHAT_ID, read_answers[LANGUAGE]['string_email']
                           + f": {data['email']}\n")
    await bot.send_message(CHAT_ID, read_answers[LANGUAGE]['string_ticket']
                           + f": {data['ticket']}")

    await message.answer(read_answers[LANGUAGE]['call_successful'],
                         reply_markup=mp.start)
    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer(read_answers[LANGUAGE]['successful_cancel'],
                         reply_markup=mp.start)


def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        support_answer, commands=["Поддержка"])

    dispatcher.register_message_handler(
        cancel_handler, commands=["cancel_2"], state='*')
    dispatcher.register_message_handler(
        cancel_handler, Text(equals="Отмена", ignore_case=True), state='*')

    dispatcher.register_message_handler(get_username, state=UserState.name)
    dispatcher.register_message_handler(get_email, state=UserState.email)
    dispatcher.register_message_handler(get_ticket, state=UserState.ticket)
