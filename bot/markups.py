from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ****************** MainMenuw12  ******************
# - Start menu -
bmenu = KeyboardButton("Меню")
bhelp = KeyboardButton("Поддержка")
startMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(bmenu, bhelp)
# - Main menu -
bwork1 = KeyboardButton("Способ 1")
bwork2 = KeyboardButton("Способ 2")
bmore = KeyboardButton("Подробнее")
bmain = KeyboardButton("⬅ Меню")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bwork1, bwork2).add(bmain)

# ****************** way1  ******************
bcancel = KeyboardButton("/cancel")
ways = ReplyKeyboardMarkup(resize_keyboard=True).add(bcancel)
bstep1 = KeyboardButton("К шагу 1")
step1 = ReplyKeyboardMarkup(resize_keyboard=True).add(bcancel, bstep1)
bstep2 = KeyboardButton("К шагу 2")
step2 = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bstep1, bstep2).add(bcancel)
bstep3 = KeyboardButton("К шагу 3")
step3 = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bstep2, bstep3).add(bcancel)
bstep4 = KeyboardButton("К шагу 4")
step4 = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bstep3, bstep4).add(bcancel)

bscript = KeyboardButton("Правила оформления")
rightscript = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bscript).add(bcancel)

baction = KeyboardButton("Команды")
fullaction = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bscript, baction).add(bcancel)

bbut = KeyboardButton("Команда «Кнопка»")
btime = KeyboardButton("Команда «Задержка»")
bswitch = KeyboardButton("Команда «Переключатель»")
bex = KeyboardButton("Пример")
allcom = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bbut, btime).add(bswitch).add(bex, bcancel)

example = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(baction, bex).add(bcancel)
bexcept = KeyboardButton("Ограничения")
bdwld = KeyboardButton("Загрузка cценария")
dwldexcept = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bex, bdwld).add(bexcept, bcancel)
dwld = ReplyKeyboardMarkup(resize_keyboard=True).add(bcancel, bdwld)
