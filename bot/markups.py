from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bmain = KeyboardButton("⬅ Меню")
"""
# - Start menu -
//bmenu = KeyboardButton("Меню")
bhelp = KeyboardButton("Поддержка")
startMenu = ReplyKeyboardMarkup(resize_keyboard= True).add(bmenu, bhelp)
"""

# - Main menu -
bwork1 = KeyboardButton("Способ 1")
bwork2 = KeyboardButton("Способ2")
mainMenu = ReplyKeyboardMarkup(resize_keyboard= True).add(bwork1, bwork2, bmain)