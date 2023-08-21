from peewee import *
from models.base_model import BaseModel


class Word(BaseModel):
    id = PrimaryKeyField(null=False)
    chat_id = CharField(max_length=100)
    text = CharField(max_length=100)

    class Meta:
        db_table = "words"
