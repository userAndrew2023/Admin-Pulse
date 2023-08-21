from telebot.types import *
from app import bot
from models.chats import Chat as ChatModel
from service import chat_service


def community_markup(message_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Добавить", callback_data=f"add_chat:{message_id}"))
    markup.add(InlineKeyboardButton("Мои чаты", callback_data=f"read_chats:{message_id}"))
    return markup


@bot.message_handler(commands=['community'])
def community(message: Message):
    message = bot.send_message(message.chat.id,
                               """Здесь вы можете добавлять и удалять свои Telegram чаты/каналы! 📢""")
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id,
                                  reply_markup=community_markup(message.message_id))


@bot.callback_query_handler(func=lambda call: "delete_chat:" in call.data)
def delete_chat(call: CallbackQuery):
    chat_model: ChatModel = chat_service.find_one(int(call.data.split(":")[1]))
    bot.leave_chat(chat_model.chat_id)
    chat_service.delete(int(call.data.split(":")[1]))
    bot.send_message(call.from_user.id, "Успешно")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: "read_chats:" in call.data)
def read_chats(call: CallbackQuery):
    chats = chat_service.find_all(call.from_user.id)
    for chat_model in chats:
        chat_model: ChatModel = chat_model
        chat = bot.get_chat(chat_model.chat_id)
        result = f"""Название: {chat.title}
Описание: {chat.description if chat.description is not None else 'Отсутствует'}"""
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("Удалить", callback_data=f"delete_chat:{chat_model.id}"))
        bot.send_message(call.from_user.id, result, reply_markup=markup)
    bot.send_message(call.from_user.id, f"У вас добавлено {len(chats)} групп")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: "add_chat:" in call.data)
def add_chat(call: CallbackQuery):
    bot.send_message(call.from_user.id, f"Чтобы добавить бота в группу/канал, сделайте его администратором")
    bot.answer_callback_query(call.id)

