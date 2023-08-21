from peewee import MySQLDatabase
from telebot import TeleBot
from data.config import *

bot = TeleBot(token=BOT_TOKEN)
db = MySQLDatabase(database=db_name, user=user, password=password, host=host)

from handlers import handler
from handlers import community_handler
from handlers import moderation_handler
from handlers import delayed_message_handler

