from peewee import *
from models.base_model import BaseModel


class Balance(BaseModel):
    id = PrimaryKeyField(null=False)
    user_id = CharField(max_length=100)
    balance = FloatField(default=0)

    class Meta:
        db_table = "balances"
