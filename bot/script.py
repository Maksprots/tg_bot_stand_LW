from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    menu_support = [
        [
            types.KeyboardButton(text="Меню"),
            types.KeyboardButton(text="Поддержка")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=menu_support,
        resize_keyboard=True
    )
    await message.answer("Выберите раздел", reply_markup=keyboard)


@dispatcher.message_handler(content_types=['document'])
async def scan_message(message: types.Message):
    document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    await message.document.download(file_info.file_path)
    await message.answer('Файл успешно сохранён')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=False)
