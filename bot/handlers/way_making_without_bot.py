from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot import markups as mp
import yaml

from bot.config import path_for_users_firmware, path_for_users_script
from bot.config import TEXT_PATH_WITHOUT
from bot.handlers.utils.building_and_loading_usr_pack import build_usr_files
from bot.create_bot import logger

LANGUAGE = 'RU'
with open(TEXT_PATH_WITHOUT, encoding='utf-8') as fh:
    dictionary_yaml_answers = yaml.safe_load(fh)


# TODO прописать рабочую откладку логов по всем исключениям
# todo перенести все состояния в отдельный файл
class ClientStatesGroup2(StatesGroup):
    nothing = State()
    board = State()
    desc = State()
    mail = State()


# Отмена загрузки файлов
async def cancel_upload_w2(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message. \
        reply(dictionary_yaml_answers[LANGUAGE]['back_to_menu'],
              reply_markup=mp.menu)
    await state.finish()


async def asking_for_email(message: types.Message) -> None:
    await ClientStatesGroup2.mail.set()
    await message.answer(dictionary_yaml_answers[LANGUAGE]['ask_email'])


# Сохранение почты
async def saving_email_addr(message: types.Message, state: FSMContext):
    user_email = message.text  # TODO ???
    if not (user_email[len(user_email) - len('@edu.hse.ru'):] == '@edu.hse.ru'
            and user_email.count('@') == 1 and user_email != '@edu.hse.ru'):
        await asking_for_email(message)
        return
    await state.update_data(email=user_email)
    await chosen_way(message=message)


async def chosen_way(message: types.Message) -> None:
    await ClientStatesGroup2.nothing.set()
    await message \
        .answer(dictionary_yaml_answers[LANGUAGE]['chosen_way_without_bot'],
                reply_markup=mp.load_firmware)


# отправка пользователем прошивки
async def invitation_to_upload_firmware(message: types.Message) -> None:
    await ClientStatesGroup2.board.set()
    await message.answer(dictionary_yaml_answers[LANGUAGE]['add_file_sof'])


# Сохранение прошивки
async def downloading_firmware(message: types.Message):
    await ClientStatesGroup2.board.set()
    await message.document.download(
        destination_file=path_for_users_firmware.format(
            message.from_user.id
        )
    )
    await message.answer(dictionary_yaml_answers[LANGUAGE]['success_load'],
                         reply_markup=mp.load_script)


async def invitation_to_upload_script(message: types.Message) -> None:
    await ClientStatesGroup2.desc.set()
    await message.answer(dictionary_yaml_answers[LANGUAGE]['script_loading'])


@logger.catch()
async def downloading_of_script(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.document.download(
        destination_file=
        path_for_users_script.format(
            message.from_user.id
        )
    )
    build_usr_files(message.from_user.id, data['email'])

    await message.answer(dictionary_yaml_answers[LANGUAGE]['file_saving'])
    await message.answer(dictionary_yaml_answers[LANGUAGE]['wait_letter'] + " "
                         + data['email'],
                         reply_markup=mp.menu)
    await state.finish()


def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        cancel_upload_w2, commands=["cancel"], state="*")
    dispatcher.register_message_handler(
        asking_for_email, Text(equals="Способ 2", ignore_case=True), state="*")
    dispatcher.register_message_handler(
        saving_email_addr,
        state=ClientStatesGroup2.mail.state)
    dispatcher.register_message_handler(
        invitation_to_upload_firmware, Text(equals="Загрузка прошивки", ignore_case=True),
        state="*")
    dispatcher.register_message_handler(
        downloading_firmware, content_types=['document'],
        state=ClientStatesGroup2.board.state)
    dispatcher.register_message_handler(
        invitation_to_upload_script, Text(equals="Загрузить cценарий", ignore_case=True),
        state="*")
    dispatcher.register_message_handler(
        downloading_of_script, content_types=['document'],
        state=ClientStatesGroup2.desc.state)
