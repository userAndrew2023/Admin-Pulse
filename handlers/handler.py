import time
import uuid

from telebot.types import *
from app import bot
from handlers import community_handler
from models.balances import Balance
from service import chat_service
from models.chats import Chat as ChatModel
from cryptomus import Client
from data.config import *

client = Client.payment(PAYMENT_KEY, MERCHANT_ID)


@bot.message_handler(commands=['start'])
def start(message: Message):
    try:
        obj: Balance = Balance.get(Balance.user_id == str(message.chat.id))
    except:
        Balance(user_id=message.chat.id).save()
    if len(message.text.split()) == 2:
        request = message.text.split()[1]
        chat_id = int(request.split("_")[-1])
        chat: ChatModel = chat_service.find_one(chat_id)
        if not chat.is_pay:
            bot.send_message(message.chat.id, "Этот канал больше не платный 🤗. Вот ссылка на него...")
            time.sleep(0.5)
            bot.send_message(message.chat.id, community_handler.generate(chat.chat_id))
            return
        bot.send_message(message.chat.id, f"Оплатите {chat.cost}$, чтобы получить доступ к каналу/группе "
                                          f"<b>{bot.get_chat(chat.chat_id).title}</b>", parse_mode="HTML")
        data = {
            'amount': str(chat.cost),
            'currency': 'USD',
            'network': 'TRON',
            'order_id': str(uuid.uuid4()),
        }
        order: dict = client.create(data)
        bot.send_message(message.chat.id, f"<b>{order.get('url')}</b>", parse_mode="HTML")
        check_url(order, chat.chat_id, message.from_user.id)
        return
    bot.send_message(message.chat.id, """🌟 Приветствуем в боте AdminPulse! Здесь вы сможете:

1️⃣ Модерировать чат
2️⃣ Делать платными приватные группы
3️⃣ Публиковать отложенный контент

Если у вас возникнут вопросы или нужна дополнительная информация, не стесняйтесь спрашивать! 😊🚀""")


def check_url(json_data: dict, chat_id, user_id: int):
    while True:
        info = client.info({
            "uuid": json_data.get("uuid"),
            "order_id": json_data.get("order_id")
        })
        if info.get("payment_status") == "paid" or info.get("payment_status") == "paid_over":
            bot.send_message(user_id, "Вы успешно оплатили платеж. Ссылка генерируется...")
            time.sleep(0.5)
            bot.send_message(user_id, community_handler.generate(chat_id))
            chat: ChatModel = chat_service.find_by_chat_id(chat_id)
            balance: Balance = Balance.get(Balance.user_id == chat.user_id)
            balance.balance += chat.cost
            balance.save()
            break
        elif info.get("payment_status") == "cancel" or info.get("payment_status") == "fail":
            break
        time.sleep(1)


@bot.message_handler(content_types=['new_chat_members'])
def bot_member_handler(message):
    if message.json['new_chat_participant']['id'] == 6427839406:
        json_message = message.json
        chat_service.add(json_message['chat']['id'], json_message['from']['id'])
        bot.send_message(json_message['from']['id'], "Вы успешно добавили меня в группу")
