import datetime

import peewee

from app import bot, db
from models.chats import Chat
from models.closed_channels import ClosedChannel
from models.delayed_messages import DelayedMessage
from models.words import Word

try:
    db.connect()
    Chat.create_table() if not Chat.table_exists() else print("Таблица chats уже создана")
    Word.create_table() if not Word.table_exists() else print("Таблица words уже создана")
    DelayedMessage.create_table() if not DelayedMessage.table_exists() else print("Таблица delayed_messages уже создана")
    ClosedChannel.create_table() if not ClosedChannel.table_exists() else print("Таблица closed_channels уже создана")
except peewee.InternalError as px:
    print(px)

bot.infinity_polling()
