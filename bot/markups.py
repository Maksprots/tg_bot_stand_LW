from aiogram.types import ReplyKeyboardMarkup
import bot.buttons as bt


start = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.menu, bt.support)

support = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.cancel_2)

menu = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(bt.way_1, bt.way_2).add(bt.back2menu)

ways = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.cancel)
step_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.cancel, bt.to_step_1)

step_2 = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(bt.to_step_1, bt.to_step_2).add(bt.cancel)

step_3 = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(bt.to_step_2, bt.to_step_3).add(bt.cancel)

step_4 = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(bt.to_step_3, bt.to_step_4).add(bt.cancel)

check_rules = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(bt.rules).add(bt.cancel)

check_commands = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(bt.rules, bt.commands).add(bt.cancel)

commands_list = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(bt.button_cmd, bt.wait_cmd) \
    .add(bt.switch_cmd).add(bt.example_cmd, bt.cancel)

example = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(bt.commands, bt.example_cmd).add(bt.cancel)

loading_or_scopes = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(bt.example_cmd, bt.loading_script).add(bt.scopes, bt.cancel)
loading = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bt.cancel, bt.loading_script)

load_firmware = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bt.cancel, bt.loading_firmware)

load_script = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(bt.loading_firmware, bt.loading_script_2).add(bt.cancel)
