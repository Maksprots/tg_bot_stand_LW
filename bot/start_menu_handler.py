import yaml

from aiogram import types, Dispatcher
from bot.create_bot import bot
from bot import markups as mp
from aiogram.dispatcher.filters import Text
from handlers.support_implementation import support_answer
from config import TEXT_PATH_WITH


LANGUAGE = 'RU'

with open(TEXT_PATH_WITH,
          encoding='UTF-8') as f:
    read_answers = yaml.safe_load(f)


async def cmd_start(message: types.Message) -> None:
    await message.answer(read_answers[LANGUAGE]['start_menu_greetings'],
                         reply_markup=mp.start)


# @dispatcher.message_handler()
async def bot_message(message: types.Message) -> None:
    if message.text == "Меню":
        await bot.send_message(message.from_user.id,
                               read_answers[LANGUAGE]['stand_options'],
                               reply_markup=mp.menu)
    elif message.text == "⬅ Меню":
        await bot.send_message(message.from_user.id, "⬅ Меню",
                               reply_markup=mp.menu)


def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(cmd_start,
                                        commands=["start"])
    dispatcher.register_message_handler(bot_message,
                                        Text(equals="Меню",
                                             ignore_case=True))
    dispatcher.register_message_handler(cmd_start,
                                        Text(equals="⬅ Меню",
                                             ignore_case=True))
    dispatcher.register_message_handler(support_answer,
                                        Text(equals="Поддержка",
                                             ignore_case=True))
