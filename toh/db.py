import os
import requests
import redis
import time
import telebot
from telebot import types

API_TOKEN = '1395353835:AAG2S0pc3uUL2oGbnQLBycnECAj_SqZv4uI'
bot = telebot.TeleBot(API_TOKEN)
r = redis.from_url(
    "redis://h:p8dcd27beb1689f9ada4a3f8652a1c99fbf852394cdd2d38fb8ec2d6de60c5622@ec2-52-204-185-105.compute-1.amazonaws.com:20719")

db_keys = r.keys(pattern="*")


def send_announcments(bot_message):
    for keys in db_keys:
        keys_values = r.get(keys).decode("UTF-8")
        print(keys_values)
        send_text = 'https://api.telegram.org/bot' + API_TOKEN + \
            '/sendMessage?chat_id=' + keys_values + '&text=' + bot_message
        print(send_text)
        response = requests.get(send_text)
        print(response.json())
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        markup.add("/acknowledged")
        bot.send_message(
            keys_values, "To acknowledge, reply with \n/acknowledged", reply_markup=markup)
        time.sleep(1)


__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

bot_message = open(os.path.join(__location__, "message_bot.txt"))

text_content = bot_message.read()

send_announcments(bot_message=text_content)
