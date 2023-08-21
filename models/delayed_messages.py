from peewee import *

from models.base_model import BaseModel


class DelayedMessage(BaseModel):
    id = PrimaryKeyField(null=False)
    chat_id = CharField(max_length=100)
    text = CharField(max_length=100)
    date_time = DateTimeField(null=False)

    class Meta:
        db_table = "delayed_messages"
