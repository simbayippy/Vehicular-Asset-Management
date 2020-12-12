import os
import schedule
import telebot
from telebot import types, TeleBot
from flask import Flask, request
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import schedule
from pprint import pprint

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

sheet = client.open('Test Sheet').get_worksheet(0)


time1 = "07:30"  # to update by user
time2 = "16:00"  # to update by user
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
        url='https://guarded-reaches-36373.herokuapp.com/' + API_TOKEN)
    return "!", 200


class User:
    def __init__(self, vtype):
        self.vtype = vtype


@ bot.message_handler(commands=['start', 'submitanother'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    markup.add('MDTV', 'OUV', 'CBT AMB', '6 TON')
    msg = bot.reply_to(
        message, "Welcome to MRF's Vehicle Maintenance Bot. \n\nSelect vehicle type: ", reply_markup=markup)
    bot.register_next_step_handler(msg, process_vtype_step)


def process_vtype_step(message):
    try:
        chat_id = message.chat.id
        vtype = message.text
        print('Vehicle Type: ' + vtype)
        user = User(vtype)
        user_dict[chat_id] = user
        user.vtype = vtype
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        if vtype == 'MDTV':
            markup.add('41001', '41002', '41003', '41004', '41005')
            msg = bot.reply_to(
                message, 'Enter Vehicle number:', reply_markup=markup)

        elif vtype == 'OUV':
            markup.add('34375', '33780')
            msg = bot.reply_to(
                message, 'Enter Vehicle number:', reply_markup=markup)

        elif vtype == 'CBT AMB':
            markup.add('34827', '34670', '34789')
            msg = bot.reply_to(
                message, 'Enter Vehicle number:', reply_markup=markup)

        elif vtype == '6 TON':
            markup.add('21820', '21948', '21845', '21832',
                       '21946', '21789', '21943', '21827')
            msg = bot.reply_to(
                message, 'Enter Vehicle number:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_vnum_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


def process_vnum_step(message):
    try:
        chat_id = message.chat.id
        vnum = message.text
        user = user_dict[chat_id]
        user.vnum = vnum
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('JIT', 'BOC')
        msg = bot.reply_to(message, 'Enter task: ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_task_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


@bot.message_handler(commands=['resenddate'])
def process_task_step(message):
    try:
        task = message.text
        if task == 'JIT':
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.task = task
            msg = bot.reply_to(
                message, 'Enter date of task in the form \nDD/MM/YY: ')
        elif task == 'BOC':
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.task = task
            msg = bot.reply_to(
                message, 'Enter date of task in the form \nDD/MM/YY: ')
        elif task == '/resenddate':
            msg = bot.reply_to(
                message, 'Enter date of task in the form \nDD/MM/YY: ')

        bot.register_next_step_handler(msg, process_datetask_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


def process_datetask_step(message):
    try:
        datetask = message.text
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        chat_id = message.chat.id
        user = user_dict[chat_id]
        if len(datetask) == 8:
            markup.add('Yes', 'No')
            msg = bot.reply_to(message,  'Please verify that the following information is correct\n\nYour vehicle is: ' + user.vtype + '\nVehicle number is: ' +
                               user.vnum + '\n\nTask is: ' + user.task + '\nDate of ' + user.task + ' is: ' + datetask, reply_markup=markup)
            user.datetask = datetask
            print(message.chat.id)

            bot.register_next_step_handler(msg, process_verify_step)
        else:
            markup.add('/resenddate')
            msg = bot.reply_to(
                message, 'Date has to be in the form \nDD/MM/YY. To re enter date, type \n/resenddate.', reply_markup=markup)
            bot.register_next_step_handler(msg, process_task_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


def process_verify_step(message):
    try:
        chat_id = message.chat.id
        verify = message.text
        user = user_dict[chat_id]
        user.verify = verify
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        vehicle = user.vtype + user.vnum
        user.vehicle = vehicle
        if verify == 'Yes':
            markup.add('/submitanother')
            bot.send_message(
                chat_id, 'Input finished. To submit another, type \n/submitanother', reply_markup=markup)
            if user.task == 'JIT':
                updateJITdate(message)
            if user.task == 'BOC':
                updateBOCdate(message)
        else:
            markup.add('/start')
            bot.reply_to(
                message, ' Please restart this form by typing \n/start', reply_markup=markup)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')

# sheets stuff


def comparedate(date_time_str1, date_time_str2):
    datetime_obj1 = datetime.datetime.strptime(
        date_time_str1, '%d/%m/%y')
    d1 = datetime_obj1.date()
    datetime_obj2 = datetime.datetime.strptime(
        date_time_str2, '%d/%m/%y')
    d2 = datetime_obj2.date()
    diff = (abs(d2-d1).days)
    return (diff)


def updatedate():
    i = 2
    currentdatestr = datetime.datetime.today().strftime('%d/%m/%y')
    while i < 20:
        jit = sheet.cell(i, 2).value
        boc = sheet.cell(i, 3).value
        jit_diff = comparedate(jit, currentdatestr)
        boc_diff = comparedate(boc, currentdatestr)
        sheet.update_cell(i, 4, jit_diff)
        sheet.update_cell(i, 5, boc_diff)
        i += 1
    print("updated " + currentdatestr)


def reminder():
    i = 2
    while i < 20:
        # jit
        days_to_jit = int(sheet.cell(i, 7).value)
        if days_to_jit <= reminderdays:
            vnojit = sheet.cell(i, 1).value
        # boc
        days_to_boc = int(sheet.cell(i, 8).value)
        if days_to_boc <= reminderdays:
            vnoboc = sheet.cell(i, 1).value
        # combined
        if days_to_jit <= reminderdays or days_to_boc <= reminderdays:
            bot.send_message(-490206159,
                             "_" + vnojit + "_  has " + str(days_to_boc) + " days left till the next JIT deadline \n" + "_" + vnoboc + "_  has " + str(days_to_jit) + " days left till the next JIT deadline")
        i += 1
    print('done')


def checkdate():
    values = sheet.get("F2:H19")
    valuenew = "\n".join(map(str, values)).replace(
        '[', '').replace(']', '').replace("'", '')
    # if want each line 2 people, .replace('[', '   '])
    bot.send_message(-490206159,
                     '**Vehicle Maintanence** \n(Vc, days to JIT, days to BOC) \n\n' + valuenew)


checkdate()
# updates the BOC date to current date when called, takes in vehicle string (as in first column of spreadsheet)


def updateBOCdate(vehicle):
    chat_id = vehicle.chat.id
    user = user_dict[chat_id]
    if user.vehicle == "MDTV41001":
        sheet.update_cell(2, 3, user.datetask)
    elif user.vehicle == "MDTV41002":
        sheet.update_cell(3, 3, user.datetask)
    elif user.vehicle == "MDTV41003":
        sheet.update_cell(4, 3, user.datetask)
    elif user.vehicle == "MDTV41004":
        sheet.update_cell(5, 3, user.datetask)
    elif user.vehicle == "MDTV41005":
        sheet.update_cell(6, 3, user.datetask)
    elif user.vehicle == "OUV34375":
        sheet.update_cell(7, 3, user.datetask)
    elif user.vehicle == "OUV33780":
        sheet.update_cell(8, 3, user.datetask)
    elif user.vehicle == "CBT AMB34827":
        sheet.update_cell(9, 3, user.datetask)
    elif user.vehicle == "CBT AMB34670":
        sheet.update_cell(10, 3, user.datetask)
    elif user.vehicle == "CBT AMB34789":
        sheet.update_cell(11, 3, user.datetask)
    elif user.vehicle == "6 TON21820":
        sheet.update_cell(12, 3, user.datetask)
    elif user.vehicle == "6 TON21948":
        sheet.update_cell(13, 3, user.datetask)
    elif user.vehicle == "6 TON21845":
        sheet.update_cell(14, 3, user.datetask)
    elif user.vehicle == "6 TON21832":
        sheet.update_cell(15, 3, user.datetask)
    elif user.vehicle == "6 TON21946":
        sheet.update_cell(16, 3, user.datetask)
    elif user.vehicle == "6 TON21789":
        sheet.update_cell(17, 3, user.datetask)
    elif user.vehicle == "6 TON21943":
        sheet.update_cell(18, 3, user.datetask)
    elif user.vehicle == "6 TON21827":
        sheet.update_cell(19, 3, user.datetask)

    updatedate()


# updates JIT date to current date when called, takes in vehicle string (as in first column of spreadsheet)
def updateJITdate(vehicle):
    chat_id = vehicle.chat.id
    user = user_dict[chat_id]
    if user.vehicle == "MDTV41001":
        sheet.update_cell(2, 2, user.datetask)
    elif user.vehicle == "MDTV41002":
        sheet.update_cell(3, 2, user.datetask)
    elif user.vehicle == "MDTV41003":
        sheet.update_cell(4, 2, user.datetask)
    elif user.vehicle == "MDTV41004":
        sheet.update_cell(5, 2, user.datetask)
    elif user.vehicle == "MDTV41005":
        sheet.update_cell(6, 2, user.datetask)
    elif user.vehicle == "OUV34375":
        sheet.update_cell(7, 2, user.datetask)
    elif user.vehicle == "OUV33780":
        sheet.update_cell(8, 2, user.datetask)
    elif user.vehicle == "CBT AMB34827":
        sheet.update_cell(9, 2, user.datetask)
    elif user.vehicle == "CBT AMB34670":
        sheet.update_cell(10, 2, user.datetask)
    elif user.vehicle == "CBT AMB34789":
        sheet.update_cell(11, 2, user.datetask)
    elif user.vehicle == "6 TON21820":
        sheet.update_cell(12, 2, user.datetask)
    elif user.vehicle == "6 TON21948":
        sheet.update_cell(13, 2, user.datetask)
    elif user.vehicle == "6 TON21845":
        sheet.update_cell(14, 2, user.datetask)
    elif user.vehicle == "6 TON21832":
        sheet.update_cell(15, 2, user.datetask)
    elif user.vehicle == "6 TON21946":
        sheet.update_cell(16, 2, user.datetask)
    elif user.vehicle == "6 TON21789":
        sheet.update_cell(17, 2, user.datetask)
    elif user.vehicle == "6 TON21943":
        sheet.update_cell(18, 2, user.datetask)
    elif user.vehicle == "6 TON21827":
        sheet.update_cell(19, 2, user.datetask)

    updateBOCdate(vehicle)
    updatedate()


# updates days left at the start of every day
schedule.every().day.at("00:01").do(updatedate)
# checks date and sends push message accordingly
schedule.every().day.at(time1).do(checkdate)
# checks date and sends push message accordingly
schedule.every().day.at(time2).do(checkdate)

while 1:  # keeps the schedule running
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
