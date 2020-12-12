import telebot
from telebot import types
import time
import os
from flask import Flask, request
import redis
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time
import requests
import itertools


scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

server = Flask(__name__)
API_TOKEN = '1364940659:AAHaEM0tWAxElCMy08zduOnC5cWd9vB4eP8'
bot = telebot.TeleBot(API_TOKEN)
user_dict = {}


spreadsheet = client.open('sheets')
sheet = spreadsheet.get_worksheet(3)


class User:
    def __init__(self, platoon):
        self.platoon = platoon
        self.name = None


@ bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Welcome to MRF's Recall Bot. \n
Enter passcode:
""")
    bot.register_next_step_handler(msg, process_passcode_step)


def process_passcode_step(message):
    try:
        passcode = message.text
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        if passcode == 'abc':
            markup.add('38th', '39th', '40th')
            msg = bot.reply_to(
                message, "Enter your platoon: ", reply_markup=markup)

            chat_id = str(message.chat.id)
            try:
                sheet.find(chat_id)
                print('yes')
                pass

            except gspread.exceptions.CellNotFound:  # or except gspread.CellNotFound:
                print('No')
                user_id = [message.chat.id]
                sheet.insert_row(user_id, 1)
                print(user_id)

            bot.register_next_step_handler(msg, process_pre_platoon_step)
        else:
            markup.add('/start')
            msg = bot.reply_to(
                message, 'Incorrect passcode. Check with your PC/FS for the correct passcode. \n(passcode is case sensitive) \n\nPlease restart the bot by typing /start.', reply_markup=markup)
    except Exception as e:
        pass


@ bot.message_handler(commands=['hi'])
def send_hi(message):
    msg = bot.reply_to(message, """\
Welcome to the admin side of MRF's recall bot. \n
Upon completion this will send a recall message to all troopers in the unit. *Only authorized personnel* can access this option \n
Enter password:
""", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_password_step)


def process_password_step(message):
    try:
        chat_id = message.chat.id
        password = message.text
        user = User(password)
        user_dict[chat_id] = user
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        if password == 'a':
            msg = bot.reply_to(
                message, 'Enter recall message: ', reply_markup=markup)
            bot.register_next_step_handler(msg, process_recallmsg)

        else:
            markup.add('/send_recall')
            msg = bot.reply_to(
                message, 'Incorrect passcode. Check with PC/FS for the correct passcode. \n(passcode is case sensitive) \n\nPlease restart the bot by typing \n /send_recall.', reply_markup=markup)

    except Exception as e:
        pass


def process_recallmsg(message):
    try:
        chat_id = message.chat.id
        recallmsg = message.text
        user = user_dict[chat_id]
        user.recallmsg = recallmsg
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('Yes', 'No')
        msg = bot.reply_to(
            message,  ' Please verify that the following information is *correct*\n \nRecall message is:\n\n' + user.recallmsg, reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_verifyrecall_step)
        bot.register_next_step_handler(msg, sendtoallusers)

    except Exception as e:
        pass


def sendtoallusers(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    all_userids = sheet.get_all_values()
    flat_list = []
    for sublist in all_userids:
        for item in sublist:
            flat_list.append(item)
    print(flat_list)
    additionalmsg = '\n\nTo acknowledge, reply with \n/acknowledged'
    markup = types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True)
    markup.add('/acknowledged')
    for x in flat_list:
        bot.send_message(x, user.recallmsg + additionalmsg,
                         reply_markup=markup)
        print(x)


def sendtoallusers2():

    all_userids = sheet.get_all_values()
    flat_list = []
    for sublist in all_userids:
        for item in sublist:
            flat_list.append(item)
    print(flat_list)
    additionalmsg = '\n\nTo acknowledge, reply with \n/acknowledged'
    markup = types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True)
    markup.add('/acknowledged')
    for x in flat_list:
        bot.send_message(x, '*You have been activated, return to camp immediately*\n\n_This message will be sent every minute until we have received your reply_ ' +
                         additionalmsg, reply_markup=markup, parse_mode='Markdown')
        print(x)


def process_verifyrecall_step(message):
    try:
        chat_id = message.chat.id
        verifyrecall = message.text
        user = user_dict[chat_id]
        user.verifyrecall = verifyrecall
        markup = types.ReplyKeyboardMarkup(
            row_width=2, one_time_keyboard=True)
        if verifyrecall == 'Yes':
            k = 0
            while k < 2:

                sendtoallusers2()

                msg = bot.reply_to(
                    message,  'Recall sent.', reply_markup=markup)
                msg = bot.send_message(
                    chat_id, "A list of troopers ETA will also be sent to _admin group_", parse_mode='Markdown')

                time.sleep(10)
                k += 0.5
                print(k)
        else:
            markup.add('/send_recall')
            msg = bot.reply_to(
                message,  'Please restart this form.', reply_markup=markup)
    except Exception as e:
        pass


@ bot.message_handler(commands=['acknowledged', 'submitanother', 'restart'])
def send_welcome(message):

    a = str(message.chat.id)
    cell = sheet.find(a)
    cell_address = "%s" % (cell.row)
    cell2 = int(cell_address)
    print(cell_address)
    sheet.delete_rows(cell2)

    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    markup.add('38th', '39th', '40th')
    msg = bot.reply_to(message, """\
Please enter your details. \n
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

        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        if platoon == '38th':
            markup.add('abc', 'dec', 'cgd')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        elif platoon == '39th':
            markup.add('Sailesh', 'Gi Suk', 'Kian Siang', 'Abilash', 'Firdaus', 'Jeng Yi', 'Shariff', 'Ray', 'Jian Hao', 'Baodo', 'Ilyas', 'Mazlan', 'Ji Hao', 'Prithiv', 'Balaji', 'Elden',
                       'Sadiq', 'Ismail', 'Beaumont', 'Teng Hee', 'Kim', 'Zahid', 'Ramlan', 'Harith', 'Hamidi', 'Santhosh', 'Wei Tao', 'Farhan', 'Enzo', 'Syazwan', 'Idris', 'Perumal', 'Ezuan', 'Danish')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        elif platoon == '40th':
            markup.add('Steven', 'Ethan', 'Rizwan', 'Anish', 'Kaiser', 'Zulfan', 'Qi Rui', 'Chen Jun', 'Josh', 'Asher', 'Simba', 'Abhi', 'Ming Ju', 'Sim Wei', 'Shinn', 'Kyaw Soe', 'Frederick', 'Ming Xuan',
                       'Cedric', 'Shannon', 'Min Hong', 'Darius', 'Sidharth', 'Jazz', 'Ranveer', 'Chao Ming', 'Abdiel', 'Royston', 'Kester', 'Wendell', 'Ryan', 'Paolo', 'Sibi', 'Benjamin', 'Ming Hui', 'William')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        else:
            pass
        bot.register_next_step_handler(msg, process_naming_step)
    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/restart')


bot.polling()
