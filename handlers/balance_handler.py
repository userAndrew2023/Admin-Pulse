import uuid

from telebot.types import *
from app import bot
from models.balances import Balance
from cryptomus import Client
from data.config import *


@bot.message_handler(commands=['balance'])
def balance(message: Message):
    try:
        obj: Balance = Balance.get(Balance.user_id == str(message.chat.id))
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("Вывести", callback_data=f"withdraw:{message.chat.id}")) if obj.balance > 1 else ""
        bot.send_message(message.chat.id, f"Ваш баланс: {obj.balance}$", reply_markup=markup)
    except:
        Balance(user_id=str(message.chat.id)).save()
        obj: Balance = Balance.get(Balance.user_id == str(message.chat.id))
        bot.send_message(message.chat.id, f"Ваш баланс: {obj.balance}$")


@bot.callback_query_handler(func=lambda call: "withdraw:" in call.data)
def withdraw(call: CallbackQuery):
    bot.send_message(call.from_user.id, "Введите количество в $. Число должно быть без точки с запятой")
    bot.register_next_step_handler(call.message, money_entered)


def money_entered(message: Message):
    try:
        obj: Balance = Balance.get(Balance.user_id == str(message.chat.id))
        int(message.text)
        money = float(message.text)
        if money > obj.balance:
            bot.send_message(message.chat.id, "Ошибка. Введено число, большее чем баланс")
            return
        bot.send_message(message.chat.id, "Введите кошелек USDT-TRC20")
        bot.register_next_step_handler(message, wallet_entered, *[money])
    except:
        bot.send_message(message.chat.id, "Ошибка")


def wallet_entered(message: Message, money: float):
    client = Client.payout(PAYOUT_KEY, MERCHANT_ID)
    data = {
        'amount': str(money * 0.96),
        'currency': 'USDT',
        'network': 'TRON',
        'order_id': str(uuid.uuid4()),
        'address': message.text
    }
    client.create(data)
    q: Balance = Balance.get(Balance.user_id == message.chat.id)
    q.balance -= money
    q.save()
    bot.send_message(message.chat.id, "Успешно")
