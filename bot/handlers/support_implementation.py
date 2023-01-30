from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from bot.create_bot import bot
from bot import markups as mp
import yaml
import os


load_dotenv()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

TEXT_PATH = '/static/texts/answers_text_with_bot.yaml'
LANGUAGE = 'RU'
CHAT_ID = '-1001859110427'


with open(os.getcwd() + TEXT_PATH,
          encoding='UTF-8') as f:
    read_answers = yaml.safe_load(f)


class UserState(StatesGroup):
    name = State()
    email = State()
    ticket = State()


async def support_anwser(message: types.Message, state: FSMContext):
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
    await message.answer(f"Имя: {data['username']}\n"
                         f"Адрес: {data['email']}\n"
                         f"Текст проблемы: {data['ticket']}")
    await bot.send_message(CHAT_ID, f'Имя: {data["username"]}\n'
                                    f'Адрес: {data["email"]}\n'
                                    f'Текст проблемы: {data["ticket"]}')
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
        support_anwser, commands=["Поддержка"])

    dispatcher.register_message_handler(
        cancel_handler, commands=["cancel_2"], state='*')
    dispatcher.register_message_handler(
        cancel_handler, Text(equals="Отмена", ignore_case=True), state='*')

    dispatcher.register_message_handler(get_username, state=UserState.name)
    dispatcher.register_message_handler(get_email, state=UserState.email)
    dispatcher.register_message_handler(get_ticket, state=UserState.ticket)
