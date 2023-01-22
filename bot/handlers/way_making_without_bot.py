from aiogram import Dispatcher, types
from bot.create_bot import bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot import markups as mp
import yaml
LANGUAGE = 'RU'
filename = 'bot\\static\\texts\\answers_text_way2.yaml'


def read_from_yaml(filepath):
    with open(filepath, encoding='utf-8') as fh:
        dictionary_data = yaml.safe_load(fh)
        return dictionary_data


dictionary_yaml_answers = read_from_yaml(filename)


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


# начало работы в ветви
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
    file_info = await bot.get_file(document_id)
    await message.document.download(file_info.file_path)
    await message.answer(dictionary_yaml_answers[LANGUAGE]['file_saving'])
    await message.answer(dictionary_yaml_answers[LANGUAGE]['wait_letter'],
                         reply_markup=mp.menu)
    await state.finish()


def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        cancel_load_w2, commands=["cancel"], state="*")
    dispatcher.register_message_handler(
        choose_way, Text(equals="Способ 2", ignore_case=True), state="*")
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
