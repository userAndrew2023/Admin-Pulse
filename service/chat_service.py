from models.chats import Chat


def add(chat_id, user_id):
    Chat(chat_id=chat_id, user_id=user_id).save()


def find_one(id: int):
    return Chat.get(Chat.id == id)


def find_by_chat_id(id):
    return Chat.get(Chat.chat_id == id)


def find_all_all():
    return Chat.select()


def find_all(user_id: int):
    return Chat.select().where(Chat.user_id == user_id)


def reverse_pay(id: int):
    chat: Chat = Chat.get(Chat.id == id)
    chat.is_pay = not chat.is_pay
    chat.save()


def cost(id: int, new: float):
    chat: Chat = Chat.get(Chat.id == id)
    chat.cost = new
    chat.save()


def delete(id: int):
    Chat.get(Chat.id == id).delete_instance()
