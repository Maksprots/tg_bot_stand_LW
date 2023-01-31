from aiogram import Dispatcher, types
from bot.create_bot import bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot import markups as mp
import yaml
import os

TEXT_PATH = '/static/texts/answers_text_with_bot.yaml'

with open(os.getcwd() + TEXT_PATH,
          encoding='UTF-8') as f:
    read_answers = yaml.safe_load(f)


class ClientStatesGroup(StatesGroup):
    nothing = State()
    board = State()
    desc = State()
    mail = State()


# Отмена загрузки файлов
async def cancel_load(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply(read_answers['RU']['back_to_menu'],
                        reply_markup=mp.menu)
    await state.finish()


async def ask_for_email(message: types.Message) -> None:
    await ClientStatesGroup.mail.set()
    await message.answer(read_answers['RU']['ask_email'])


# Сохранение почты
async def save_mail(message: types.Message, state: FSMContext):
    user_email = message.text
    if 'edu.hse.ru' not in user_email:
        await ask_for_email(message)
        await save_mail(message)
    await state.update_data(email=user_email)
    await choose_way_1(message=message)


async def choose_way_1(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(read_answers['RU']['chosen_way_with_bot'])
    await message.answer(read_answers['RU']['chosen_way_with_bot_2'],
                         reply_markup=mp.step_1)


# Подготовка проекта пользователем
async def fstep1(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(read_answers['RU']['step_1'],
                         reply_markup=mp.step_2)


# Объяснение о прошивке пользователю
async def fstep2(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(read_answers['RU']['step_2'],
                         reply_markup=mp.step_3)


# Отправка пользователем прошивки
async def start_load_board(message: types.Message) -> None:
    await ClientStatesGroup.board.set()
    await message.answer(read_answers['RU']['step_3'])


# Сохранение прошивки
async def load_board(message: types.Message):
    await ClientStatesGroup.board.set()
    board_id = message.document.file_id
    board_info = await bot.get_file(board_id)
    await message.document.download(board_info.file_path)
    await message.answer(read_answers['RU']['success_load'],
                         reply_markup=mp.step_4)


# отправка пользователем сценария
async def learn_more_script(message: types.Message) -> None:
    await ClientStatesGroup.desc.set()
    await message.answer(read_answers['RU']['need_a_script'])
    await message.answer(read_answers['RU']['need_a_script_2'])
    await message.answer(read_answers['RU']['need_a_script_3'],
                         reply_markup=mp.check_rules)


# ознакомление с правилами оформления
async def start_learn_script(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(read_answers['RU']['script_rules'])
    await message.answer(read_answers['RU']['script_rules_1'])
    await message.answer(read_answers['RU']['script_rules_2'])
    await message.answer(read_answers['RU']['script_rules_3'])
    await message.answer(read_answers['RU']['script_rules_4'])
    await message.answer(read_answers['RU']['go_to_learning_commands'],
                         reply_markup=mp.check_commands)


# начало ознакомления с командами в целом
async def learn_commands(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(read_answers['RU']['first_step_learning_commands'])
    await message.answer(read_answers['RU']['first_step_learning_commands_2'],
                         reply_markup=mp.commands_list)


# ознакомление с командой «Кнопка»
async def learn_command1(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(read_answers['RU']['second_step_learning_commands'])
    await message.answer(read_answers['RU']['second_step_learning_commands_2'])
    await message.answer(read_answers['RU']['second_step_learning_commands_3'])
    await message.answer(read_answers['RU']['second_step_learning_commands_4'])
    await message.answer(read_answers['RU']['second_step_learning_commands_5'])
    await message.answer(read_answers['RU']['first_step_learning_commands_6'],
                         reply_markup=mp.commands_list)


# ознакомление с командой «Переключатель»
async def learn_command2(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(read_answers['RU']['third_step_learning_commands'])
    await message.answer(read_answers['RU']['third_step_learning_commands_2'])
    await message.answer(read_answers['RU']['third_step_learning_commands_3'])
    await message.answer(read_answers['RU']['third_step_learning_commands_4'])
    await message.answer(read_answers['RU']['third_step_learning_commands_5'])
    await message.answer(read_answers['RU']['third_step_learning_commands_6'],
                         reply_markup=mp.commands_list)


# ознакомление с командой «Задержка»
async def learn_comand3(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(read_answers['RU']['fourth_step_learning_commands'])
    await message.answer(read_answers['RU']['fourth_step_learning_commands_2'])
    await message.answer(read_answers['RU']['fourth_step_learning_commands_3'])
    await message.answer(read_answers['RU']['fourth_step_learning_commands_4'])
    await message.answer(read_answers['RU']['fourth_step_learning_commands_5'])
    await message.answer(read_answers['RU']['fourth_step_learning_commands_6'],
                         reply_markup=mp.commands_list)


# пример составления сценария
async def learn_example(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await bot.send_photo(message.from_user.id,
                         photo=open(os.getcwd()
                                    + '/static/images/script.jpg', "rb"),
                         caption="Пример составления сценария:")
    await message.answer(read_answers['RU']['scripting_process'])
    await message.answer(read_answers['RU']['scripting_process_2'])
    await message.answer(read_answers['RU']['scripting_process_3'],
                         reply_markup=mp.loading_or_scopes)


# ознакомление с ограничениями
async def learn_exception(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(read_answers['RU']['restriction_warning'])
    await message.answer(read_answers['RU']['restriction_warning_1'])
    await message.answer(read_answers['RU']['restriction_warning_2'])
    await message.answer(read_answers['RU']['restriction_warning_3'])
    await message.answer(read_answers['RU']['restriction_warning_4'])
    await message.answer(read_answers['RU']['restriction_warning_5'])
    await message.answer(read_answers['RU']['restriction_warning_6'])
    await message.answer(read_answers['RU']['restriction_warning_6'],
                         reply_markup=mp.loading)


# шаг загрузки сценария
async def start_load_desc(message: types.Message) -> None:
    await ClientStatesGroup.desc.set()
    await message.answer(read_answers['RU']['script_loading'],
                         reply_markup=mp.ways)


# Сохранить документ
async def scan_message(message: types.Message, state: FSMContext):
    document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    await message.document.download(file_info.file_path)
    await message.answer(read_answers['RU']['file_saving'])
    await message.answer(read_answers['RU']['success_message'],
                         reply_markup=mp.menu)
    await state.finish()


# регестрация хэндлеров
def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        cancel_load, commands=["cancel"], state="*")
    # dispatcher.register_message_handler(
    #    choose_way_1, Text(equals=read_answers['RU']['to_first_method'],
    #                      ignore_case=True), state="*")
    dispatcher.register_message_handler(
        ask_for_email, Text(equals="Способ 1", ignore_case=True), state="*")
    dispatcher.register_message_handler(
        save_mail,
        state=ClientStatesGroup.mail.state)
    dispatcher.register_message_handler(
        fstep1, Text(equals=read_answers['RU']['to_step_one'],
                     ignore_case=True), state="*")
    dispatcher.register_message_handler(
        fstep2, Text(equals=read_answers['RU']['to_step_two'],
                     ignore_case=True), state="*")
    dispatcher.register_message_handler(
        start_load_board, Text(equals=read_answers['RU']['to_step_three'],
                               ignore_case=True), state="*")
    dispatcher.register_message_handler(
        load_board, content_types=['document'],
        state=ClientStatesGroup.board.state)
    dispatcher.register_message_handler(
        learn_more_script, Text(equals=read_answers['RU']['to_step_four'],
                                ignore_case=True), state="*")
    dispatcher.register_message_handler(
        start_learn_script, Text(equals=read_answers['RU']['design_rules'],
                                 ignore_case=True), state="*")
    dispatcher.register_message_handler(
        learn_commands, Text(equals=read_answers['RU']['possible_commands'],
                             ignore_case=True), state="*")
    dispatcher.register_message_handler(
        learn_command1, Text(equals=read_answers['RU']['option_button'],
                             ignore_case=True), state="*")
    dispatcher.register_message_handler(
        learn_command2, Text(equals=read_answers['RU']['option_switch'],
                             ignore_case=True), state="*")
    dispatcher.register_message_handler(
        learn_comand3, Text(equals=read_answers['RU']['option_delay'],
                            ignore_case=True), state="*")
    dispatcher.register_message_handler(
        learn_example, Text(equals=read_answers['RU']['introductory_example'],
                            ignore_case=True), state="*")
    dispatcher.register_message_handler(
        learn_exception, Text(
            equals=read_answers['RU']['possible_restrictions'],
            ignore_case=True), state="*")
    dispatcher.register_message_handler(
        start_load_desc, Text(equals=read_answers['RU']['start_load_script'],
                              ignore_case=True), state="*")
    dispatcher.register_message_handler(
        scan_message, content_types=['document'],
        state=ClientStatesGroup.desc.state)
