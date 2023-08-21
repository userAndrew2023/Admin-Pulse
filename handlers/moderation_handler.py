from telebot.types import *

from app import bot
from models.chats import Chat as ChatModel
from models.words import Word
from service import chat_service, word_service


def is_chat_id_in_group(user_id):
    for i in chat_service.find_all_all():
        chat_model: ChatModel = i
        if int(chat_model.chat_id) == int(user_id):
            return True
    return False


@bot.message_handler(commands=['moderation'])
def moderation(message: Message):
    chats = chat_service.find_all(message.from_user.id)
    for chat_model in chats:
        chat_model: ChatModel = chat_model
        chat = bot.get_chat(chat_model.chat_id)
        result = f"""Канал/группа: <b>{chat.title}</b>"""
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Добавить слова", callback_data=f"add_words:{chat_model.id}"))
        markup.add(InlineKeyboardButton("Посмотреть/Удалить слова", callback_data=f"delete_words:{chat_model.id}"))
        markup.add(InlineKeyboardButton("Удалить все слова", callback_data=f"delete_all_words:{chat_model.id}"))
        bot.send_message(message.from_user.id, result, reply_markup=markup, parse_mode="HTML")
    bot.send_message(message.chat.id, "😊 Это раздел модерации. Вы можете добавлять списки запрещенных слов. 👮‍♂️🚫")


@bot.message_handler(func=lambda message: is_chat_id_in_group(message.chat.id))
def moderation1(message: Message):
    chat_id = chat_service.find_by_chat_id(str(message.chat.id)).id
    if message.text.lower() in [i.text for i in list(word_service.find_all(str(chat_id)))]:
        bot.delete_message(message.chat.id, message.id)


@bot.callback_query_handler(func=lambda call: "delete_words:" in call.data)
def delete_words(call: CallbackQuery):
    chat_id = call.data.split(":")[1]
    m = InlineKeyboardMarkup(row_width=1)
    words = word_service.find_all(chat_id)
    for i in words:
        word: Word = i
        m.add(InlineKeyboardButton(word.text, callback_data=f"delete_word:{word.id}"))
    if len(words) == 0:
        bot.send_message(call.from_user.id, "Слов пока нет")
    else:
        bot.send_message(call.from_user.id, "Выберите слово из списка, чтобы удалить", reply_markup=m)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: "add_words:" in call.data)
def add_words(call: CallbackQuery):
    chat_id = call.data.split(":")[1]
    bot.send_message(call.from_user.id, "Введите слово или слова через запятую и пробел. Например: кот, собака, мышь")
    bot.register_next_step_handler(call.message, word_entered, *[chat_id])


def word_entered(message: Message, chat_id):
    [Word(chat_id=chat_id, text=i).save() for i in message.text.split(", ")]
    bot.send_message(message.chat.id, "Успешно")


@bot.callback_query_handler(func=lambda call: "delete_word:" in call.data)
def delete_word(call: CallbackQuery):
    chat_id = call.data.split(":")[1]
    Word.delete().where(Word.id == int(chat_id)).execute()
    bot.send_message(call.from_user.id, "Успешно")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: "delete_all_words:" in call.data)
def delete_all_words(call: CallbackQuery):
    chat_id = call.data.split(":")[1]
    Word.delete().where(Word.chat_id == chat_id).execute()
    bot.send_message(call.from_user.id, "Успешно")
    bot.answer_callback_query(call.id)
