import datetime

from models.delayed_messages import DelayedMessage


def add(chat_id: str, text: str, date_time: datetime.datetime):
    DelayedMessage(chat_id=chat_id, text=text, date_time=date_time).save()


def find_one(id: int):
    return DelayedMessage.get(DelayedMessage.id == id)


def find_one_chat_id(chat_id: str):
    return DelayedMessage.get(DelayedMessage.chat_id == chat_id)


def find_all_all():
    return DelayedMessage.select()


def find_all(chat_id):
    return DelayedMessage.select().where(DelayedMessage.chat_id == str(chat_id))


def delete(id: int):
    DelayedMessage.get(DelayedMessage.id == id).delete_instance()
