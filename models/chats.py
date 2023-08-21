import datetime

from models.base_model import BaseModel
from peewee import *


class Chat(BaseModel):
    id = PrimaryKeyField(null=False)
    chat_id = CharField(max_length=100)
    user_id = CharField(max_length=100)

    class Meta:
        db_table = "chats"
