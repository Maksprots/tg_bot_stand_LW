#  Telegram bot for working with a remote laboratory stand

## Windows

1. Download and install python 3.10 for windows:
tick "Add python to PATH" !!
[python 3.9](https://www.python.org/downloads/release/python-390/)

2. There are also several ways to install Git on Windows. 
The official build is available for download on the official Git website. 
Just go to [link](https://git-scm.com/download/win) and the download will start automatically. 
Note that this is a separate project called Git for Windows; 
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
