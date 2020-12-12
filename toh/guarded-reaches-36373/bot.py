import telebot
from telebot import types
import time
import os
from flask import Flask, request
import redis

server = Flask(__name__)
API_TOKEN = '1395353835:AAG2S0pc3uUL2oGbnQLBycnECAj_SqZv4uI'
bot = telebot.TeleBot(API_TOKEN)
user_dict = {}
r = redis.from_url(os.environ.get(
    "redis://h:p8f7365885545205bf5931da9c158c1ca19e264030061cdfd9d2d827755fab3bb@ec2-52-4-66-210.compute-1.amazonaws.com:12229"))


@ server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@ server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(
        url='https://guarded-reaches-36373.herokuapp.com/' + API_TOKEN)
    return "!", 200


class User:
    def __init__(self, platoon):
        self.platoon = platoon
        self.name = None


# Handle '/start' and '/help'
@ bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    markup.add('38th', '39th', '40th')
    msg = bot.reply_to(message, """\
Welcome to MRF's Recall Bot. \n
Enter your platoon:
""", reply_markup=markup)
    bot.register_next_step_handler(msg, process_platoon_step)


def process_platoon_step(message):
    try:
        chat_id = message.chat.id
        platoon = message.text
        print('Users platoon: ' + platoon)
        print(chat_id)
        user = User(platoon)
        user_dict[chat_id] = user
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        if platoon == '38th':
            markup.add('abc', 'dec', 'cgd')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        elif platoon == '39th':
            markup.add('simba', 'kaiser', 'ming hui')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        elif platoon == '40th':
            markup.add('q', 'q', 'g s')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        else:
            pass
        bot.register_next_step_handler(msg, process_name_step)
    except Exception as e:
        bot.reply_to(message, 'Invalid Input, please restart by typing /start')


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        print('Users name: '+name)
        print(chat_id)
        user = user_dict[chat_id]
        user.name = name
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        markup.add('Yes', 'No')
        msg = bot.reply_to(message,  ' Please verify that the following information is correct\n \n Your platoon is: ' + user.platoon +
                           '\n Your name is: ' + user.name, reply_markup=markup)
        bot.register_next_step_handler(msg, process_verification_step)
        r.set(chat_id, name)
    except Exception as e:
        bot.reply_to(message, 'Invalid Input, please restart by typing /start')


def process_verification_step(message):
    try:
        chat_id = message.chat.id
        verification = message.text
        print('Details correrct?: ' + verification)
        print(chat_id)
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        if verification == 'Yes':
            markup.add('0-10mins', '10-20mins', '20-30mins', '30-40mins',
                       '40-50mins', '50-60mins', '60-70mins', '70-80mins')
            msg = bot.reply_to(
                message,  ' What is ur ETA to Nee Soon Camp?', reply_markup=markup)
            bot.register_next_step_handler(msg, process_time_step)
        else:
            markup.add('/start')
            msg = bot.reply_to(
                message,  ' Please restart this form', reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, 'Invalid Input, please restart by typing /start')


def process_time_step(message):
    try:
        chat_id = message.chat.id
        time = message.text
        print('Users ETA: ' + time)
        print(chat_id)
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        location_button = types.KeyboardButton(
            'Send location', request_location=True)
        markup.add(location_button)
        msg = bot.reply_to(
            message,  ' Please send your current location', reply_markup=markup)
        bot.register_next_step_handler(msg, process_location_step)

    except Exception as e:
        bot.reply_to(message, 'Invalid Input, please restart by typing /start')


def process_location_step(message):
    try:
        chat_id = message.chat.id
        location = (message.location.latitude, message.location.longitude)
        print(location)
        print(chat_id)
        # alternative form for location
        # print("{0}, {1}".format(message.location.latitude, message.location.longitude))
        chat_id = message.chat.id
        msg = bot.reply_to(
            message,  'Please return to camp safely and as soon as possible, goodluck! :)')
        time.sleep(2)
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('/start')
        bot.send_message(
            chat_id, 'Input finish. To restart please type /start', reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, 'Invalid Input, please restart by typing /start')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
