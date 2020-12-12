import telebot
from telebot import types
import time
import os
from flask import Flask, request
import redis
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open('sheets').get_worksheet(1)
val = sheet.get("A2:C37")
valnew = "\n\n".join(map(str, val)).replace(
    '[', '').replace(']', '').replace("'", '')
# if want each line 2 people, .replace('[', '   '])
#sheet.update_acell('D3', "yes")


def update_eta_column():
    # to update sheets as empty in second column
    cell_list = sheet.range('B2:B46')

    # Update values
    for cell in cell_list:
        cell.value = "yet to update"

    # Send update in batch mode
    sheet.update_cells(cell_list)


update_eta_column()

# 1364940659: AAHaEM0tWAxElCMy08zduOnC5cWd9vB4eP8


def process_time_step(message):
    try:
        chat_id = message.chat.id
        time = message.text
        print('Users ETA: ' + time)
        print(chat_id)
        user = user_dict[chat_id]
        user.time = time
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        location_button = types.KeyboardButton(
            'Send location', request_location=True)
        markup.add(location_button)
        msg = bot.reply_to(
            message,  'Please send your current location', reply_markup=markup)
        bot.register_next_step_handler(msg, process_location_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/restart')


def process_location_step(message):
    try:
        chat_id = message.chat.id
        location = "{0},{1}".format(
            message.location.latitude, message.location.longitude)
        user = user_dict[chat_id]
        user.location = "https://www.google.com/maps/place/"+location
