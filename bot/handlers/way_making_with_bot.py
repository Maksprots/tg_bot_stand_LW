from aiogram import Dispatcher, types
from bot.create_bot import bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot import markups as mp


# Отмена загрузки файлов
async def cancel_load(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('Вернулись в меню', reply_markup=mp.menu)
    await state.finish()


# назначение состояний
class ClientStatesGroup(StatesGroup):
    nothing = State()
    board = State()
    desc = State()


# выбрали способ 1
async def choose_way1(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer("Вы выбрали пошаговое выполнение работы вместе с "
                         "ботом на удаленном стенде\n"
                         "Чтобы приступить к работе нажмите к «шагу 1»\n"
                         "Чтобы вернуться в главное меню нажмите «cancel»\n",
                         reply_markup=mp.step_1)


# Подготовка проекта пользователем
async def fstep1(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer("Подготовьте проект для платы De10Lite\n"
                         "Если готовы, перходите к шагу 2\n"
                         "Иначе вернитесь к шагу 1", reply_markup=mp.step_2)


# Объяснение о прошивке пользователю
async def fstep2(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer(
        "Скомпилируйте проект и получите файл прошивки, он будет по умолчанию"
        " находиться в папке output_files и иметь расширение «.sof».\n",
        reply_markup=mp.step_3)


# Отправка пользователем прошивки
async def start_load_board(message: types.Message) -> None:
    await ClientStatesGroup.board.set()
    await message.answer(" Прикрепите файл прошивки с раширением «.sof»")


# Сохранение прошивки
async def load_board(message: types.Message):
    await ClientStatesGroup.board.set()
    board_id = message.document.file_id
    board_info = await bot.get_file(board_id)
    await message.document.download(board_info.file_path)
    await message.answer("Прошивка успешно сохранена\n"
                         "Переходите к шагу 4", reply_markup=mp.step_4)


# отправка пользователем сценария
async def learn_more_script(message: types.Message) -> None:
    await ClientStatesGroup.desc.set()
    await message.answer("Дальше нужно написать сценарий, который будет "
                         "содержать команды управления платой ПЛИС.\n"
                         "Для этого нужно ознакомиться с правилами "
                         "оформления сценария и допустимыми командами.\n\n"
                         "Ознакомьтесь с оформлением сценария.\n\n",
                         reply_markup=mp.check_rules)


# ознакомление с правилами оформления
async def start_learn_script(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer("Правила оформления сценария:\n\n"
                         "1) Каждая новая команда обязательно начинается с "
                         "новой строки\n\n"
                         "2) Номер пина, на который осуществляется "
                         "воздействие, не может быть меньше 1 или больше 8, "
                         "в противном случае, в файле ошибок, будет записаны"
                         " данная ошибка и указание на строку, в которой она "
                         "встретилась.\n\n"
                         "3) В конце файла сценария в обязательном порядке "
                         "должна присутствовать команда «end», "
                         "которая означает конец распознаваемого сценария."
                         "\n\n"
                         "4) Имеется возможность установить задержку "
                         "(команда delay) на какую-либо команду. "
                         "Она будет применяться к той команде, которая "
                         "находится на строчку выше. \n\n")
    await message.answer("Когда ознакомитесь с правилами оформления сценария"
                         " переходите к изучению доступных команд\n",
                         reply_markup=mp.check_commands)


# начало ознакомления с командами в целом
async def learn_comands(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer("Список команд, которые выполняет стенд:\n"
                         "1) «Кнопка + номер пина». \n"
                         "2) «Переключатель + номер пина».\n"
                         "3) «Задержка + время». \n\n"
                         "Чтобы ознакомиться с командами нажмите на кнопку,"
                         " соответстующую команде\n"
                         "Когда ознакомитесь с доступными командами,"
                         " переходите к примеру\n", reply_markup=mp.commands_list)


# ознакомление с командой «Кнопка»
async def learn_comand1(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer("«Кнопка + номер пина» \n"
                         "\nВозможные записи: \nbutton, but, But, Button\n"
                         "Номер пина записывается либо через пробел, "
                         "либо слитно\n"
                         "\nФункции:\n"
                         "Производит переключение указанного пина из 0 в 1 на "
                         "0,5 секунды, после этого происходит переключение "
                         "обратно в состояние 0. \n"
                         "После выполнения команды проходит задержка 0,5 "
                         "секунды\n\n"
                         "Чтобы ознакомиться с другими командами нажмите"
                         " на кнопку соответстующую им\n"
                         "Когда ознакомитесь с доступными командами, "
                         "переходите к примеру\n", reply_markup=mp.commands_list)


# ознакомление с командой «Переключатель»
async def learn_comand2(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer("«Переключатель + номер пина».\n"
                         "\nВозможные записи:\nswitch, sw, Sw, Switch\n"
                         "Номер пина записывается либо через пробел, "
                         "либо слитно\n"
                         "\nФункции:\n"
                         "Производит переключение указанного пина в "
                         "противоположное от текущего состояние, "
                         "при этом обратное переключение будет вызвано"
                         " только повторным применением данной команда "
                         "с данным пином.\n\n"
                         "Чтобы ознакомиться с другими командами нажмите "
                         "на кнопку соответстующую им\n"
                         "Когда ознакомитесь с доступными командами, "
                         "переходите к примеру\n", reply_markup=mp.commands_list)


# ознакомление с командой «Задержка»
async def learn_comand3(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer("«Задержка + время». \n"
                         "\nВозможные записи:\ndelay\n"
                         "Через пробел указывается время в секундах для "
                         "задержки.\n"
                         "\nФункции: \nСлужит для приостановки чтения файла "
                         "сценария.Может использоваться после любой команды."
                         "\nДанную команду рекомендуется применять в случае "
                         "необходимости наблюдать за работой прошивки при "
                         "удержании того или иного пина.\n\n"
                         "Чтобы ознакомиться с другими командами нажмите на"
                         " кнопку соответстующую им\n"
                         "Когда ознакомитесь с доступными командами, "
                         "переходите к примеру\n",
                         reply_markup=mp.commands_list)


# пример составления сценария
async def learn_example(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await bot.send_photo(message.from_user.id,
                         photo=open("photos/script.jpg", "rb"),
                         caption="Пример составления сценария:")
    await message.answer("Когда ознакомитесь с примером, приступайте к "
                         "оформлению собственного сценария. "
                         "\nОн должен быть в формате «.txt» и "
                         "соответствовать всем выше перечисленным "
                         "требованиям.\n"
                         "\nТакже можете ознакомиться с техническими "
                         "ограничениями стенда, для этого нажмите"
                         " «Ограничения»."
                         "\nЛибо преступите к загрузке сценария.",
                         reply_markup=mp.loading_or_scopes)


# ознакомление с ограничениями
async def learn_exception(message: types.Message) -> None:
    await ClientStatesGroup.nothing.set()
    await message.answer("Основные	ограничения:\n"
                         "1) Максимальное количество команд управления"
                         " – 50 штук;\n"
                         "2) Максимальное время компиляции проекта"
                         " – 10 минут;\n"
                         "3) Максимальная длительность единичной задержки"
                         " – 30 секунд;\n"
                         "4) Максимальная длительность записываемого видео"
                         " – 2 минуты;\n"
                         "5) После повторной отправки прошивки на обработку"
                         " результаты предыдущей обработки удаляются;\n"
                         "6) Нельзя указывать индексы кнопок и переключателей"
                         " меньше 1 и больше 8.\n"
                         "7) При неправильном написании команд они не "
                         "будут выполнены", reply_markup=mp.loading)


# шаг загрузки сценария
async def start_load_desc(message: types.Message) -> None:
    await ClientStatesGroup.desc.set()
    await message.answer("Прикрепите сценарий!", reply_markup=mp.ways)


# Сохранить документ
async def scan_message(message: types.Message, state: FSMContext):
    document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    await message.document.download(file_info.file_path)
    await message.answer('Сценарий успешно сохранен')
    await message.answer('У вас всё получилось🎉', reply_markup=mp.menu)
    await state.finish()


# регестрация хэндлеров
def registration_of_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        cancel_load, commands=["cancel"], state="*")
    dispatcher.register_message_handler(
        choose_way1, Text(equals="Способ 1", ignore_case=True), state="*")
    dispatcher.register_message_handler(
        fstep1, Text(equals="К шагу 1", ignore_case=True), state="*")
    dispatcher.register_message_handler(
        fstep2, Text(equals="К шагу 2", ignore_case=True), state="*")
    dispatcher.register_message_handler(
        start_load_board, Text(equals="К шагу 3", ignore_case=True), state="*")
    dispatcher.register_message_handler(
        load_board, content_types=['document'],
        state=ClientStatesGroup.board.state)
    dispatcher.register_message_handler(
        learn_more_script, Text(equals="К шагу 4", ignore_case=True),
        state="*")
    dispatcher.register_message_handler(
        start_learn_script, Text(equals="Правила оформления",
                                 ignore_case=True), state="*")
    dispatcher.register_message_handler(
        learn_comands, Text(equals="Команды", ignore_case=True), state="*")
    dispatcher.register_message_handler(
        learn_comand1, Text(equals="Команда «Кнопка»", ignore_case=True),
        state="*")
    dispatcher.register_message_handler(
        learn_comand2, Text(equals="Команда «Переключатель»",
                            ignore_case=True), state="*")
    dispatcher.register_message_handler(
        learn_comand3, Text(equals="Команда «Задержка»", ignore_case=True),
        state="*")
    dispatcher.register_message_handler(
        learn_example, Text(equals="Пример", ignore_case=True), state="*")
    dispatcher.register_message_handler(
        learn_exception, Text(equals="Ограничения", ignore_case=True),
        state="*")
    dispatcher.register_message_handler(
        start_load_desc, Text(equals="Загрузка cценария", ignore_case=True),
        state="*")
    dispatcher.register_message_handler(
        scan_message, content_types=['document'],
        state=ClientStatesGroup.desc.state)
