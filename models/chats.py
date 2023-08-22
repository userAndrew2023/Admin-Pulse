import datetime
from peewee import *
from models.base_model import BaseModel


class Chat(BaseModel):
    id = PrimaryKeyField(null=False)
    chat_id = CharField(max_length=100)
    user_id = CharField(max_length=100)
    is_pay = BooleanField(default=False)
    cost = FloatField(null=True)

    class Meta:
        db_table = "chats"
