# файл для админ зоны бота

from aiogram import Dispatcher, types
from bot.create_bot import bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot import markups as mp
import yaml
import os

from bot.config import TEXT_PATH_WITH
from bot.config import path_for_users_firmware, path_for_users_script
from bot.config import TEXT_PATH_WITHOUT
from bot.handlers.utils.building_and_loading_usr_pack import build_usr_files


class ClientStatesGroup(StatesGroup):
    auth = State()
    board = State()
    desc = State()
    mail = State()


async def singing_up(message: types.Message):
    print(message.from_user.id)
    await ClientStatesGroup.auth.set()


def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        singing_up, Text(equals='admin'),
        state='*')
