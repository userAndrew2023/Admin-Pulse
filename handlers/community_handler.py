from telebot.types import *
from app import bot
from models.chats import Chat as ChatModel
from service import chat_service


def community_markup(message_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Добавить", callback_data=f"add_chat:{message_id}"))
    markup.add(InlineKeyboardButton("Мои чаты", callback_data=f"read_chats:{message_id}"))
    return markup


@bot.message_handler(commands=['vip'])
def vip(message: Message):
    bot.send_message(message.chat.id, "Перейдите сюда: /community")


@bot.message_handler(commands=['community'])
def community(message: Message):
    message = bot.send_message(message.chat.id,
                               """Здесь вы можете добавлять и удалять свои Telegram чаты/каналы! 📢. Если вы хотите чтобы в вашего бота можно было зайти за деньги, после добавления, нажмите кнопку 'Сделать платным'. Комиссия будет 4% при выводе средств""")
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
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Удалить", callback_data=f"delete_chat:{chat_model.id}"))
        if not chat_model.is_pay:
            markup.add(InlineKeyboardButton("Сделать платным", callback_data=f"make_pay:{chat_model.id}"))
        else:
            markup.add(InlineKeyboardButton("Сделать бесплатным", callback_data=f"make_pay:{chat_model.id}"))
        bot.send_message(call.from_user.id, result, reply_markup=markup)
    bot.send_message(call.from_user.id, f"У вас добавлено {len(chats)} групп")
    bot.answer_callback_query(call.id)


def generate(chat_id):
    return bot.export_chat_invite_link(chat_id=chat_id, usage_limit=1)


@bot.callback_query_handler(func=lambda call: "make_pay:" in call.data)
def make_pay(call: CallbackQuery):
    if not chat_service.find_one(int(call.data.split(":")[1])).is_pay:
        bot.send_message(call.from_user.id, "Введите цену в долларах (например: 9.5)")
        bot.register_next_step_handler(call.message, price_entered, *[int(call.data.split(":")[1]), call.message.id])
    else:
        chat_service.reverse_pay(int(call.data.split(":")[1]))
        chat_service.cost(int(call.data.split(":")[1]), 0)
        bot.send_message(call.from_user.id, "Успешно")
        bot.answer_callback_query(call.id)


def price_entered(message: Message, chat_id, msg_id):
    try:
        cost = float(message.text)
        if cost < 5:
            bot.send_message(message.chat.id, "Стоимость должна превышать 5$")
            return
    except:
        bot.send_message(message.chat.id, "Ошибка")
        return
    chat_service.cost(chat_id, cost)
    chat_service.reverse_pay(chat_id)
    bot.send_message(message.chat.id, "Успешно")
    bot.send_message(message.chat.id, "Чтобы клиент купил получил доступ к закрытому каналу, дайте ему вот эту ссылку: \n"
                                      f"<b><code>https://t.me/pulse_of_creator_bot?start=vip_group_{chat_id}</code></b>", parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: "add_chat:" in call.data)
def add_chat(call: CallbackQuery):
    bot.send_message(call.from_user.id, f"Чтобы добавить бота в группу/канал, сделайте его администратором. "
                                        f"Если вы хотите чтобы в вашего бота можно было зайти за деньги, после добавления, нажмите кнопку 'Сделать платным'")
    bot.answer_callback_query(call.id)
