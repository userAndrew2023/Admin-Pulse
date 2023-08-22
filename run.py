import datetime

import peewee

from app import bot, db
from models.balances import Balance
from models.chats import Chat
from models.delayed_messages import DelayedMessage
from models.words import Word

try:
    db.connect()
    Chat.create_table() if not Chat.table_exists() else print("Таблица chats уже создана")
    Word.create_table() if not Word.table_exists() else print("Таблица words уже создана")
    Balance.create_table() if not Balance.table_exists() else print("Таблица balances уже создана")
    DelayedMessage.create_table() if not DelayedMessage.table_exists() else print("Таблица delayed_messages уже создана")
except peewee.InternalError as px:
    print(px)

bot.infinity_polling()
