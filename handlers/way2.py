from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

#@dispatcher.message_handler(Text(equals="Способ 2", ignore_case=True))
async def way2(message: types.Message) -> None:
    await message.answer("В разработке...\n")

def register_handlers_way2(dispatcher : Dispatcher):
    dispatcher.register_message_handler(way2, Text(equals="Способ 2", ignore_case=True))