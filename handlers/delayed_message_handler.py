import base64
import datetime
import threading
import time

from telebot.types import *

from app import bot
from models.delayed_messages import DelayedMessage
from service import chat_service, delayed_message_service
from models.chats import Chat as ChatModel


@bot.message_handler(commands=['delayed'])
def delayed(message: Message):
    chats = chat_service.find_all(message.from_user.id)
    for chat_model in chats:
        chat_model: ChatModel = chat_model
        chat = bot.get_chat(chat_model.chat_id)
        result = f"""Канал/группа: <b>{chat.title}</b>"""
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Добавить отложенное сообщение", callback_data=f"add_delayed:{chat_model.id}"))
        markup.add(InlineKeyboardButton("Посмотреть/Удалить отложенные сообщения", callback_data=f"delete_delayed:{chat_model.id}"))
        bot.send_message(message.from_user.id, result, reply_markup=markup, parse_mode="HTML")
    bot.send_message(message.chat.id, "📌 Это раздел отложенные сообщения. Здесь вы сможете публиковать контент в ваши сообщества через какой-то промежуток времени. ⏰🚀")


@bot.callback_query_handler(func=lambda call: "add_delayed:" in call.data)
def add_delayed(call: CallbackQuery):
    chat_id = call.data.split(":")[1]
    bot.send_message(call.from_user.id, "Введите текст сообщения")
    bot.register_next_step_handler(call.message, text_entered, *[chat_id])


def text_entered(message: Message, chat_id):
    bot.send_message(message.chat.id, "Введите дату и время в формате 21-08-2023 12:13:19. Если вы введете время, меньшее чем сейчас. Сообщение отправится мгновенно")
    bot.register_next_step_handler(message, date_entered, *[chat_id, message.text])


def date_entered(message: Message, chat_id, text):
    to_format = "%d-%m-%Y %H:%M:%S"
    try:
        timing: datetime.datetime = datetime.datetime.strptime(message.text, to_format)
        bot.send_message(message.chat.id, "Успешно")
        bot.send_message(message.chat.id, f"Ваше сообщение '{text}' отправиться в {timing}")
        delayed_message_service.add(chat_id=chat_id, text=text, date_time=timing)
        threading.Thread(target=timer(timing, chat_id)).start()
    except:
        bot.send_message(message.chat.id, "Ошибка")


def timer(date_time: datetime.datetime, chat_id):
    while True:
        if datetime.datetime.now() >= date_time:
            try:
                message: DelayedMessage = delayed_message_service.find_one_chat_id(chat_id)
                chat: ChatModel = chat_service.find_one(int(chat_id))
                if message:
                    bot.send_message(chat.chat_id, message.text)
                    delayed_message_service.delete(message.id)
            except:
                pass
            break
        time.sleep(1)


@bot.callback_query_handler(func=lambda call: "delete_delayed:" in call.data)
def delete_delayed(call: CallbackQuery):
    chat_id = call.data.split(":")[1]
    for i in delayed_message_service.find_all(chat_id):
        msg: DelayedMessage = i
        res = f"""Сообщение: *{msg.text}*
Дата и время: *{msg.date_time}*"""
        bot.send_message(call.from_user.id, res, parse_mode="markdown", reply_markup=InlineKeyboardMarkup()
                         .add(InlineKeyboardButton("Удалить", callback_data=f"delete_one_delayed:{msg.id}")))
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: "delete_one_delayed:" in call.data)
def delete_one_delayed(call: CallbackQuery):
    id_ = call.data.split(":")[1]
    delayed_message_service.delete(int(id_))
    bot.send_message(call.from_user.id, "Успешно")
    bot.answer_callback_query(call.id)
