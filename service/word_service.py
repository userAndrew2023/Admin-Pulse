from models.words import Word


def add(chat_id, text):
    Word(chat_id=chat_id, text=text).save()


def find_one(id: int):
    return Word.get(Word.id == id)


def find_all_all():
    return Word.select()


def find_all(chat_id):
    return Word.select().where(Word.chat_id == str(chat_id))


def delete(id: int):
    Word.get(Word.id == id).delete_instance()
