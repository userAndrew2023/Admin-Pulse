import peewee

from app import bot, db
from models.chats import Chat
from models.words import Word

try:
    db.connect()
    Chat.create_table() if not Chat.table_exists() else print("Таблица chats уже создана")
    Word.create_table() if not Word.table_exists() else print("Таблица words уже создана")
except peewee.InternalError as px:
    print(px)

bot.infinity_polling()
