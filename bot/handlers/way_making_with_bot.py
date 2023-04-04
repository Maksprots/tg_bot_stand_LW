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

with open(TEXT_PATH_WITH,
          encoding='UTF-8') as f:
    read_answers = yaml.safe_load(f)


with open(TEXT_PATH_WITHOUT, encoding='utf-8') as fh:
    dictionary_yaml_answers = yaml.safe_load(fh)

#todo перенести все состояния в отдельный файл
class ClientStatesGroup(StatesGroup):
    nothing = State()
    board = State()
    desc = State()
    mail = State()


# Отмена загрузки файлов
async def cancel_upload(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply(read_answers['RU']['back_to_menu'],
                        reply_markup=mp.menu)
    await state.finish()


async def asking_for_email(message: types.Message) -> None:
    await ClientStatesGroup.mail.set()
    await message.answer(read_answers['RU']['ask_email'])


# Сохранение почты
async def saving_email_addr(message: types.Message, state: FSMContext):
    user_email = message.text # TODO лишняя переенная что ли
    if not (user_email[len(user_email) - len('@edu.hse.ru'):] == '@edu.hse.ru'
            and user_email.count('@') == 1 and user_email != '@edu.hse.ru'):
        await asking_for_email(message)
        return
    await state.update_data(email=user_email)
    await chosen_way(message=message)


async def chosen_way(message: types.Message) -> None:
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
async def invitation_to_upload_firmware(message: types.Message) -> None:
    await ClientStatesGroup.board.set()
    await message.answer(read_answers['RU']['step_3'])


# Сохранение прошивки
async def downloading_firmware(message: types.Message):
    await ClientStatesGroup.board.set()
    board_id = message.document.file_id
    board_info = await bot.get_file(board_id)
    await message.document.download(board_info.file_path)
    await message.answer(read_answers['RU']['success_load'],
                         reply_markup=mp.step_4)


# отправка пользователем сценария
async def invitation_to_upload_script(message: types.Message) -> None:
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
                         photo=open(os.getcwd() #todo пути всегда в конфиге должны быть
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


# Сохранение прошивки
async def downloading_firmware(message: types.Message):
    await ClientStatesGroup.desc.set()
    await message.document.download(
        destination_file=path_for_users_firmware.format(
            message.from_user.id
        )
    )
    await message.answer(dictionary_yaml_answers['RU']['success_load'],
                         reply_markup=mp.load_script)



async def invitation_to_upload_script(message: types.Message) -> None:
    await ClientStatesGroup.desc.set()
    await message.answer(dictionary_yaml_answers['RU']['script_loading'])


async def downloading_of_script(message: types.Message, state: FSMContext):
    # TODO: вызов отправки зипника на гугл драйв
    data = await state.get_data()
    await message.document.download(
        destination_file=
        path_for_users_script.format(
            message.from_user.id
        )
    )
    build_usr_files(message.from_user.id, data['email'])

    await message.answer(dictionary_yaml_answers['RU']['file_saving'])
    await message.answer(dictionary_yaml_answers['RU']['wait_letter'] + " "
                         + data['email'],
                         reply_markup=mp.menu)
    await state.finish()



def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        cancel_upload, commands=["cancel"], state="*")
    dispatcher.register_message_handler(
        asking_for_email, Text(equals="Способ 1", ignore_case=True), state="*")
    dispatcher.register_message_handler(
        saving_email_addr,
        state=ClientStatesGroup.mail.state)
    dispatcher.register_message_handler(
        fstep1, Text(equals=read_answers['RU']['to_step_one'],
                     ignore_case=True), state="*")
    dispatcher.register_message_handler(
        fstep2, Text(equals=read_answers['RU']['to_step_two'],
                     ignore_case=True), state="*")
    dispatcher.register_message_handler(
        invitation_to_upload_firmware, Text(equals=read_answers['RU']['to_step_three'],
                                            ignore_case=True), state="*")
    dispatcher.register_message_handler(
        downloading_firmware, content_types=['document'],
        state=ClientStatesGroup.board.state)
    dispatcher.register_message_handler(
        invitation_to_upload_script, Text(equals=read_answers['RU']['to_step_four'],
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
        downloading_firmware, content_types=['document'],
        state=ClientStatesGroup.desc.state)
    dispatcher.register_message_handler(
        downloading_of_script, content_types=['document'],
        state=ClientStatesGroup.desc.state)
