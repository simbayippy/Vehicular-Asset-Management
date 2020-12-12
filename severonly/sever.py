import os
import schedule
import telebot
from telebot import types, TeleBot
from flask import Flask, request
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import schedule
import requests
import emoji

# botstuff
API_TOKEN = '1095819741:AAEOiiGvXlcmRXFa_Ik2vN9e-rM_dJJs6q4'
bot = telebot.TeleBot(API_TOKEN)
user_dict = {}

# sheets stuff
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(creds)

spreadsheet = client.open('Test Sheet')
sheet = spreadsheet.sheet1

reminderdays = 3  # to update by user

server = Flask(__name__)


@ server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@ server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(
        url='https://severonly.herokuapp.com/' + API_TOKEN)
    return "!", 200


def abc():
    i = 2
    bot.send_message(-490206159,
                     emoji.emojize(':red_circle: The following vehicles have a JIT/BOC deadline in *3 or less days*'), parse_mode='Markdown')
    while i < 20:
        # jit
        days_to_jit = int(sheet.cell(i, 7).value)
        vnojit = sheet.cell(i, 6).value
        # boc
        days_to_boc = int(sheet.cell(i, 8).value)
        vnoboc = sheet.cell(i, 6).value
        # combined
        if days_to_jit <= reminderdays or days_to_boc <= reminderdays:
            bot.send_message(-490206159,
                             "_" + vnojit + "_  has " + str(days_to_jit) + " days left till the next JIT deadline \n" + "_" + vnoboc + "_  has " + str(days_to_boc) + " days left till the next BOC deadline")
        i += 1
    print('done')


def checkdate():
    sheet = client.open('Test Sheet').get_worksheet(0)
    values = sheet.get("A27:C51")
    valuenew = "\n".join(map(str, values)).replace(
        '[', '').replace(']', '').replace("'", '')
    # if want each line 2 people, .replace('[', '   '])
    currentdate = datetime.datetime.now()
    currentdatestr = datetime.datetime.strftime(currentdate, '%d/%m/%y')
    bot.send_message(
        '-490206159', emoji.emojize(':minibus: *Vehicle Maintenance* :minibus:\nList as of ' + currentdatestr + '\n\nFormat of list is as follows: \n(Vehicle, last JIT date, next JIT date)\n(Date in DD/MM) \n\n' + valuenew), parse_mode='Markdown')


checkdate()
abc()

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
