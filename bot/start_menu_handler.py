from aiogram import types, Dispatcher
from bot.create_bot import bot
from bot import markups as mp
from aiogram.dispatcher.filters import Text


async def cmd_start(message: types.Message) -> None:
    await message.answer("Вы находитесь в лаборатории для удаленного "
                         "управления стендами ПЛИС!\n"
                         "Чтобы приступить к работе выберете раздел "
                         "«Меню»\n"
                         "Если есть вопросы нажмите «Поддержка»",
                         reply_markup=mp.start)


# @dispatcher.message_handler()
async def bot_message(message: types.Message) -> None:
    if message.text == "Меню":
        await bot.send_message(message.from_user.id, "Есть два варианта работы"
                                                     " с удаленным стендом "
                                                     "лаборатории:\n\n "
                                                     "Способ 1(через бота):\n"
                                                     "Бот пошагово объясняет и"
                                                     " выполняет вашу "
                                                     "лабораторную"
                                                     "\n\n"
                                                     "Способ 2:\n"
                                                     "Какое-то описание "
                                                     "способа 2.\n\n"
                                                     "Выберите способ\n",
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
