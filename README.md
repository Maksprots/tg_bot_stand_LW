#  Telegram bot for working with a remote laboratory stand v1

## Description
Using this bot, you can perform laboratory work on remote stands. 
Version 1 uses google api, version 2 will be faster and correct 
solution. Today Google api is used in the project for quick 
integration of the bot.
## Windows

1. Download and install python 3.10 for windows:
tick "Add python to PATH" !!

  [python 3.9](https://www.python.org/downloads/release/python-390/)

2. There are also several ways to install Git on Windows. 
The official build is available for download on the official Git website. 
Just go to [link](https://git-scm.com/download/win) and the download will
start automatically. Note that this is a separate project called Git for Windows; 
for more information about it go to [link](https://gitforwindows.org)

3. Сlone the repository with gitlab:

```
git clone https://github.com/Maksprots/tg_bot_stand_LW
```

4. Install required modules from requirements.txt

```
pip install -r requirements.txt
```


## HOWTO CREATE AND CONFIGURE THIS BOT:


1. Talk to @BotFather and type "/newbot" to create a bot. Answer the questions by typing answers and pressing enter.

2. Start a chat to your bot's name (for ex. @gb-to-telegram) and press start button

3. Start another chat with https://telegram.me/get_id_bot This bot will reveal your __Chat ID__

4. Create an env file and put your bot's ID into the TELEGRAM_BOT_ID variable

5. Also create a channel to which the bot will forward messages from support and put its id into the CHAT_ID variable in the env file


## RUNING THE BOT:
```
python run.py
```

### Useed moduls
```
aiogram
api google drive
api google sheets
```
___

#  Телеграм бот для работы с удаленной лабораторией

## Описание
При помощи этого бота можно выпольнять лабораторные работы на
удаленных стендах. В верисии 1 используется  google api в версии
2 будет более быстрое и правильное решение. Сегодня гугл апи 
используется в проекте для быстрогой инеграции бота.
## Windows

1. Загрузите и установите Python 3.10 для Windows:
отметьте «Добавить python в PATH» !!

  [python 3.9](https://www.python.org/downloads/release/python-390/)

2. Вот также несколько способов установки Git в Windows.
Официальная сборка доступна для скачивания на официальном сайте Git.
Просто перейдите по [ссылке](https://git-scm.com/download/win), и загрузка начнется 
автоматически. Обратите внимание, что это отдельный проект под названием Git для Windows;
для получения дополнительной информации перейдите по [ссылке] (https://gitforwindows.org)

3. Склонируйте репозиторий с GitLab:
```
git clone https://github.com/Maksprots/tg_bot_stand_LW
```

4. Установите необходимые модули с помощью _requirements.txt_:

```
pip install -r requirements.txt
```


## Создание и подготовка бота к запуску:

1. Напишите  @BotFather и введите «/newbot», чтобы создать бота. Ответьте на вопросы и нажмите Enter.

2. Начните чат с именем вашего бота (например, @gb-to-telegram) и нажмите кнопку запуска.

3. Начните другой чат с https://telegram.me/get_id_bot. Этот бот покажет ваш __ID чата__

4. Также создайте канал, на который бот будет пересылать сообщения от службы поддержки и 
укажите его id в переменной CHAT_ID в файле env, получите айди этого чата с помошью пункта _3_

5. Создайте файл env и поместите идентификатор вашего бота в переменную TELEGRAM_BOT_ID.


### Используемые модули
```
aiogram
api google drive
api google sheets
```

## Запуск бота:

```
python run.py
```
