from aiogram import Dispatcher, types
from bot.create_bot import bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot import markups as mp
import yaml
import os


TEXT_PATH = '/static/texts/answers_text_without_bot.yaml'
LANGUAGE = 'RU'
with open(os.getcwd() + TEXT_PATH, encoding='utf-8') as fh:
    dictionary_yaml_answers = yaml.safe_load(fh)


# Отмена загрузки файлов
async def cancel_load_w2(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message. \
        reply(dictionary_yaml_answers[LANGUAGE]['back_to_menu'],
              reply_markup=mp.menu)
    await state.finish()


# назначение состояний
class ClientStatesGroup2(StatesGroup):
    nothing = State()
    board = State()
    desc = State()
    mail = State()


async def ask_for_email(message: types.Message) -> None:
    await ClientStatesGroup2.mail.set()
    await message.answer(dictionary_yaml_answers[LANGUAGE]['ask_email'])


# Сохранение почты
async def save_mail(message: types.Message,  state: FSMContext):
    user_email = message.text
    if not(user_email[len(user_email)-len('@edu.hse.ru'):] == '@edu.hse.ru'
           and user_email.count('@') == 1 and user_email != '@edu.hse.ru'):
        await ask_for_email(message)
        await save_mail(message)
    await state.update_data(email=user_email)
    await choose_way(message=message)


async def choose_way(message: types.Message) -> None:
    await ClientStatesGroup2.nothing.set()
    await message \
        .answer(dictionary_yaml_answers[LANGUAGE]['chosen_way_without_bot'],
                reply_markup=mp.load_firmware)


# отправка пользователем прошивки
async def start_load_board(message: types.Message) -> None:
    await ClientStatesGroup2.board.set()
    await message.answer(dictionary_yaml_answers[LANGUAGE]['add_file_sof'])


# Сохранение прошивки
async def load_board(message: types.Message):
    # TODO: написать сборку зипфайла с названием по тг айди
    await ClientStatesGroup2.board.set()
    board_id = message.document.file_id
    board_info = await bot.get_file(board_id)
    await message.document.download(board_info.file_path)
    await message.answer(dictionary_yaml_answers[LANGUAGE]['success_load'],
                         reply_markup=mp.load_script)


async def start_load_desc(message: types.Message) -> None:
    await ClientStatesGroup2.desc.set()
    await message.answer(dictionary_yaml_answers[LANGUAGE]['script_loading'])


async def scan_message(message: types.Message, state: FSMContext):
    document_id = message.document.file_id
    # TODO: вызов отправки зипника на гугл драйв
    file_info = await bot.get_file(document_id)
    data = await state.get_data()
    await message.document.download(file_info.file_path)
    await message.answer(dictionary_yaml_answers[LANGUAGE]['file_saving'])
    await message.answer(dictionary_yaml_answers[LANGUAGE]['wait_letter'] + " "
                         + data['email'],
                         reply_markup=mp.menu)
    await state.finish()


def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        cancel_load_w2, commands=["cancel"], state="*")
    dispatcher.register_message_handler(
        ask_for_email, Text(equals="Способ 2", ignore_case=True), state="*")
    dispatcher.register_message_handler(
        save_mail,
        state=ClientStatesGroup2.mail.state)
    dispatcher.register_message_handler(
        start_load_board, Text(equals="Загрузка прошивки", ignore_case=True),
        state="*")
    dispatcher.register_message_handler(
        load_board, content_types=['document'],
        state=ClientStatesGroup2.board.state)
    dispatcher.register_message_handler(
        start_load_desc, Text(equals="Загрузить cценарий", ignore_case=True),
        state="*")
    dispatcher.register_message_handler(
        scan_message, content_types=['document'],
        state=ClientStatesGroup2.desc.state)
