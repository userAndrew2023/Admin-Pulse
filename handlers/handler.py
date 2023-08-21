from telebot.types import *
from app import bot
from service import chat_service


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, """🌟 Приветствуем в боте AdminPulse! Здесь вы сможете:

1️⃣ Модерировать чат (текст и картинки/GIFки)
2️⃣ Выкладывать эксклюзивный контент за деньги
3️⃣ Форматировать сообщения
4️⃣ Публиковать отложенный контент
5️⃣ Собирать статистику лайков, просмотров и подписчиков

Если у вас возникнут вопросы или нужна дополнительная информация, не стесняйтесь спрашивать! 😊🚀""")


@bot.message_handler(content_types=['new_chat_members'])
def bot_member_handler(message):
    if message.json['new_chat_participant']['id'] == 6427839406:
        json_message = message.json
        chat_service.add(json_message['chat']['id'], json_message['from']['id'])
        bot.send_message(json_message['from']['id'], "Вы успешно добавили меня в группу")
