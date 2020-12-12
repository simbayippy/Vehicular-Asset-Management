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
        url='https://mrf-vehicle-maintenance.herokuapp.com/' + API_TOKEN)
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
            markup.add('34375', '34369')
            msg = bot.reply_to(
                message, 'Enter Vehicle number:', reply_markup=markup)

        elif vtype == 'CBT AMB':
            markup.add('34827', '34670', '34770')
            msg = bot.reply_to(
                message, 'Enter Vehicle number:', reply_markup=markup)

        elif vtype == '6 TON':
            markup.add('21820', '21948', '21845', '21817',
                       '21949', '21814', '21837', '21827')
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
        user_name = message.chat.first_name
        user.name = user_name
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('JIT', 'WPT1')
        msg = bot.reply_to(message, 'Enter task: ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_task_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


@bot.message_handler(commands=['resenddate'])
def process_task_step(message):
    try:
        task = message.text
        currentdate = datetime.datetime.now()
        currentdatestr = datetime.datetime.strftime(currentdate, '%d/%m/%y')
        print(currentdatestr)
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add(currentdatestr)
        if task == 'JIT':
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.task = task
            msg = bot.reply_to(
                message, 'Enter date of JIT: \n\nDate is automatically set to '+currentdatestr + ', to edit enter the correct date in the format *DD/MM/YY*', reply_markup=markup, parse_mode='Markdown')
        elif task == 'WPT1':
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.task = task
            msg = bot.reply_to(
                message, 'Enter date of WPT1: \n\nDate is automatically set to '+currentdatestr + ', to edit enter the correct date in the format *DD/MM/YY*', reply_markup=markup, parse_mode='Markdown')
        elif task == '/resenddate':
            msg = bot.reply_to(
                message, 'Enter date of task in the format \n*DD/MM/YY: *', parse_mode='Markdown')

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
        user.datetask = datetask
        if len(datetask) == 8:
            markup.add('Full', '>3/4', '1/2 to 3/4', '<1/2')
            msg = bot.reply_to(
                message, 'Enter fuel level: \n\n_Remember to fill up if fuel level is low_', reply_markup=markup, parse_mode='Markdown')

            bot.register_next_step_handler(msg, process_fuel_step)

        else:
            markup.add('/resenddate')
            msg = bot.reply_to(
                message, emoji.emojize(':no_entry:Date has to be in the format \n*DD/MM/YY*. \n\nTo re enter date, type \n/resenddate.'), reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, process_task_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


def process_fuel_step(message):
    try:
        fuel = message.text
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fuel = fuel
        vehicle = user.vtype + user.vnum
        user.vehicle = vehicle
        if user.vehicle == "MDTV41001":
            current_hoto = sheet.acell('I2').value
            user.current_hoto = current_hoto
        elif user.vehicle == "MDTV41002":
            current_hoto = sheet.acell('I3').value
            user.current_hoto = current_hoto
        elif user.vehicle == "MDTV41003":
            current_hoto = sheet.acell('I4').value
            user.current_hoto = current_hoto
        elif user.vehicle == "MDTV41004":
            current_hoto = sheet.acell('I5').value
            user.current_hoto = current_hoto
        elif user.vehicle == "MDTV41005":
            current_hoto = sheet.acell('I6').value
            user.current_hoto = current_hoto
        elif user.vehicle == "OUV34375":
            current_hoto = sheet.acell('I7').value
            user.current_hoto = current_hoto
        elif user.vehicle == "OUV33780":
            current_hoto = sheet.acell('I8').value
            user.current_hoto = current_hoto
        elif user.vehicle == "CBT AMB34827":
            current_hoto = sheet.acell('I9').value
            user.current_hoto = current_hoto
        elif user.vehicle == "CBT AMB34670":
            current_hoto = sheet.acell('I10').value
            user.current_hoto = current_hoto
        elif user.vehicle == "CBT AMB34789":
            current_hoto = sheet.acell('I11').value
            user.current_hoto = current_hoto
        elif user.vehicle == "6 TON21820":
            current_hoto = sheet.acell('I12').value
            user.current_hoto = current_hoto
        elif user.vehicle == "6 TON21948":
            current_hoto = sheet.acell('I13').value
            user.current_hoto = current_hoto
        elif user.vehicle == "6 TON21845":
            current_hoto = sheet.acell('I14').value
            user.current_hoto = current_hoto
        elif user.vehicle == "6 TON21832":
            current_hoto = sheet.acell('I15').value
            user.current_hoto = current_hoto
        elif user.vehicle == "6 TON21946":
            current_hoto = sheet.acell('I16').value
            user.current_hoto = current_hoto
        elif user.vehicle == "6 TON21789":
            current_hoto = sheet.acell('I17').value
            user.current_hoto = current_hoto
        elif user.vehicle == "6 TON21943":
            current_hoto = sheet.acell('I18').value
            user.current_hoto = current_hoto
        elif user.vehicle == "6 TON21827":
            current_hoto = sheet.acell('I19').value
            user.current_hoto = current_hoto

        markup.add('No issues', 'Issue is as stated above')
        msg = bot.reply_to(
            message, 'Any vehicle issues to HOTO: \n\n*Current status:* ' + current_hoto + '\n\n_If there are any issues, please manually type in using your keyboard. \ne.g. dented left front tyre guard_', reply_markup=markup, parse_mode='Markdown')

        bot.register_next_step_handler(msg, process_HOTO_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, pleasee restart by typing \n/start')


def process_HOTO_step(message):
    try:
        hoto = message.text
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.hoto = hoto

        markup.add('Yes', 'No')
        if hoto == 'Issue is as stated above':
            msg = bot.reply_to(message,  emoji.emojize('Please verify that the following information is *correct*:\n\n:minibus: Vehicle is: ' + user.vtype + '\n:medical_symbol: Vehicle number is: ' +
                                                       user.vnum + '\n\n:pushpin: Task: ' + user.task + '\n:stopwatch: Date of ' + user.task + ' : ' + user.datetask + '\nFuel level: ' + user.fuel + '\n\nIssue(s): ' + user.current_hoto), reply_markup=markup, parse_mode='Markdown')
        else:
            msg = bot.reply_to(message,  emoji.emojize('Please verify that the following information is *correct*:\n\n:minibus: Vehicle is: ' + user.vtype + '\n:medical_symbol: Vehicle number is: ' +
                                                       user.vnum + '\n\n:pushpin: Task: ' + user.task + '\n:stopwatch: Date of ' + user.task + ' : ' + user.datetask + '\nFuel level: ' + user.fuel + '\n\nIssue(s): ' + user.hoto), reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_verify_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, pleasee restart by typing \n/start')


def process_verify_step(message):
    try:
        chat_id = message.chat.id
        verify = message.text
        user = user_dict[chat_id]
        user.verify = verify
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        if verify == 'Yes':
            markup.add('/submitanother')
            bot.send_message(
                chat_id, emoji.emojize(':thumbs_up: Input successfully finished. To submit another, type /submitanother \n\n_Disclaimer: Bot goes offline after 30 minutes without use. Please allocate up to 15 seconds for the bot to come back online when submitting another form_'), reply_markup=markup, parse_mode='Markdown')
            send_task_done(message)
            if user.task == 'JIT':
                updateJITdate(message)
            if user.task == 'WPT1':
                updateBOCdate(message)

            if user.hoto == 'Issue is as stated above':
                pass
            else:
                updatehoto(message)
        else:
            markup.add('/start')
            bot.reply_to(
                message, 'Please restart this form by typing \n/start', reply_markup=markup)

    except Exception as e:
        pass

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
    currentdate = datetime.datetime.now()
    currentdatestr = datetime.datetime.strftime(currentdate, '%d/%m/%y')
    while i < 20:
        jit = sheet.cell(i, 2).value
        boc = sheet.cell(i, 3).value
        jit_diff = comparedate(jit, currentdatestr)
        boc_diff = comparedate(boc, currentdatestr)
        sheet.update_cell(i, 4, jit_diff)
        sheet.update_cell(i, 5, boc_diff)
        i += 1
    print("updated " + currentdatestr)


@bot.message_handler(commands=['dateline'])
def reminder(message):
    bot.reply_to(
        message, "Dateline of JIT/WPT1 will be sent to _admin group_", parse_mode='Markdown')
    checkdate()
    abc()


def abc():
    i = 2
    bot.send_message(-490206159,
                     emoji.emojize(':red_circle: The following vehicles have a JIT/WPT1 deadline in *3 or less days*'), parse_mode='Markdown')
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
                             "_" + vnojit + "_  has " + str(days_to_jit) + " days left till the next JIT deadline \n" + "_" + vnoboc + "_  has " + str(days_to_boc) + " days left till the next WPT1 deadline")
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


@bot.message_handler(commands=['updatevehiclelist'])
def updatevehicles(message):
    markup = types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True)
    markup.add('change vehicle', 'add vehicle', 'remove vehicle')
    msg = bot.reply_to(
        message, "Select a task: ", reply_markup=markup)
    bot.register_next_step_handler(msg, process_selection)


def process_selection(message):
    chat_id = message.chat.id
    selection = message.text
    user = User(selection)
    user_dict[chat_id] = user
    user.selection = selection
    if selection == 'change vehicle':
        msg = bot.reply_to(
            message, "Enter vehicle type and number that is *to be changed*: ", parse_mode='Markdown')
    elif selection == 'add vehicle':
        msg = bot.reply_to(
            message, "Enter vehicle type and number that is *to be added*: ", parse_mode='Markdown')
    elif selection == 'remove vehicle':
        msg = bot.reply_to(
            message, "Enter vehicle type and number that is *to be removed*: ", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_change)


def process_change(message):
    oldv = message.text
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.oldv = oldv
    if user.selection == 'change vehicle':
        msg = bot.reply_to(
            message, "Enter *new* vehicle type and number: ", parse_mode='Markdown')
    elif user.selection == 'add vehicle':
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('Yes', 'No')
        msg = bot.reply_to(
            message, "Please verify that the vehicle type and number *to be added* is: " + oldv, reply_markup=markup, parse_mode='Markdown')
    elif user.selection == 'remove vehicle':
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('Yes', 'No')
        msg = bot.reply_to(
            message, "Please verify that the vehicle type and number *to be removed* is: " + oldv, reply_markup=markup, parse_mode='Markdown')

    bot.register_next_step_handler(msg, process_new)


def process_new(message):
    newv = message.text
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.newv = newv
    user_name = message.chat.first_name
    user.name = user_name
    markup = types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True)
    if user.selection == 'change vehicle':
        markup.add('Yes', 'No')
        msg = bot.reply_to(
            message, "Please verify the type and number of vehicle *to be changed*: \n" + user.oldv + "\n\n*New* vehicle type and number is: \n" + user.newv, reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_verify)
    elif newv == 'Yes':
        markup.add('/updatevehiclelist', '/submitanother')
        bot.send_message(
            chat_id, emoji.emojize(':thumbs_up: Input successfully finished. Please allow up to 2 days to see the change materialise within this bot. Thankyou! \n\n_To submit another vehicle change, type /updatevehiclelist_ \n_To submit a JIT/WPT1, type \n/submitanother_'), reply_markup=markup, parse_mode='Markdown')
        bot.send_message(-494978297, 'A request for ' + user.selection + ' has been sent. \n\n' +
                         'Vehicle type and number is :' + user.oldv + '\n\nRequest sent by ' + user.name)
    elif newv == 'No':
        markup.add('/updatevehiclelist')
        bot.reply_to(
            message, 'Please restart this form by typing \n/updatevehiclelist', reply_markup=markup)


def process_verify(message):
    chat_id = message.chat.id
    verification = message.text
    user = user_dict[chat_id]
    user.verification = verification
    markup = types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True)
    if verification == 'Yes':
        markup.add('/updatevehiclelist', '/submitanother')
        bot.send_message(
            chat_id, emoji.emojize(':thumbs_up: Input successfully finished. Please allow up to 2 days to see the change materialise within this bot. Thankyou! \n\n_To submit another vehicle change, type /updatevehiclelist_ \n_To submit a JIT/WPT1, type \n/submitanother_'), reply_markup=markup, parse_mode='Markdown')
        bot.send_message(-494978297, 'A request for vehicle change has been sent. \n\n' +
                         user.oldv + ' to ' + user.newv + '\n\nRequest sent by ' + user.name)
    else:
        markup.add('/updatevehiclelist')
        bot.reply_to(
            message, 'Please restart this form by typing \n/updatevehiclelist', reply_markup=markup)


def send_task_done(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    if user.hoto == 'Issue is as stated above':
        bot.send_message(-490206159, emoji.emojize(':minibus: *Vehicle type/number: *' + user.vtype + '/' + user.vnum + '\n:thumbs_up: *Task done: *' + user.task +
                                                   '\n:stopwatch: *Date of *' + user.task + '* : *' + user.datetask + '\n*Fuel level:* ' + user.fuel + '\n*Issues:* ' + user.current_hoto + '\n\n_Task completed by:_ ' + user.name), parse_mode='Markdown')
    else:
        bot.send_message(-490206159, emoji.emojize(':minibus: *Vehicle type/number: *' + user.vtype + '/' + user.vnum + '\n:thumbs_up: *Task done: *' + user.task +
                                                   '\n:stopwatch: *Date of *' + user.task + '* : *' + user.datetask + '\n*Fuel level:* ' + user.fuel + '\n*Issues:* ' + user.hoto + '\n\n_Task completed by:_ ' + user.name), parse_mode='Markdown')


def updatehoto(vehicle):
    chat_id = vehicle.chat.id
    user = user_dict[chat_id]
    if user.vehicle == "MDTV41001":
        sheet.update_cell(2, 9, user.hoto)
    elif user.vehicle == "MDTV41002":
        sheet.update_cell(3, 9, user.hoto)
    elif user.vehicle == "MDTV41003":
        sheet.update_cell(4, 9, user.hoto)
    elif user.vehicle == "MDTV41004":
        sheet.update_cell(5, 9, user.hoto)
    elif user.vehicle == "MDTV41005":
        sheet.update_cell(6, 9, user.hoto)
    elif user.vehicle == "OUV34375":
        sheet.update_cell(7, 9, user.hoto)
    elif user.vehicle == "OUV33780":
        sheet.update_cell(8, 9, user.hoto)
    elif user.vehicle == "CBT AMB34827":
        sheet.update_cell(9, 9, user.hoto)
    elif user.vehicle == "CBT AMB34670":
        sheet.update_cell(10, 9, user.hoto)
    elif user.vehicle == "CBT AMB34789":
        sheet.update_cell(11, 9, user.hoto)
    elif user.vehicle == "6 TON21820":
        sheet.update_cell(12, 9, user.hoto)
    elif user.vehicle == "6 TON21948":
        sheet.update_cell(13, 9, user.hoto)
    elif user.vehicle == "6 TON21845":
        sheet.update_cell(14, 9, user.hoto)
    elif user.vehicle == "6 TON21832":
        sheet.update_cell(15, 9, user.hoto)
    elif user.vehicle == "6 TON21946":
        sheet.update_cell(16, 9, user.hoto)
    elif user.vehicle == "6 TON21789":
        sheet.update_cell(17, 9, user.hoto)
    elif user.vehicle == "6 TON21943":
        sheet.update_cell(18, 9, user.hoto)
    elif user.vehicle == "6 TON21827":
        sheet.update_cell(19, 9, user.hoto)


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
    elif user.vehicle == "OUV34369":
        sheet.update_cell(8, 3, user.datetask)
    elif user.vehicle == "CBT AMB34827":
        sheet.update_cell(9, 3, user.datetask)
    elif user.vehicle == "CBT AMB34670":
        sheet.update_cell(10, 3, user.datetask)
    elif user.vehicle == "CBT AMB34770":
        sheet.update_cell(11, 3, user.datetask)
    elif user.vehicle == "6 TON21820":
        sheet.update_cell(12, 3, user.datetask)
    elif user.vehicle == "6 TON21948":
        sheet.update_cell(13, 3, user.datetask)
    elif user.vehicle == "6 TON21845":
        sheet.update_cell(14, 3, user.datetask)
    elif user.vehicle == "6 TON21817":
        sheet.update_cell(15, 3, user.datetask)
    elif user.vehicle == "6 TON21949":
        sheet.update_cell(16, 3, user.datetask)
    elif user.vehicle == "6 TON21814":
        sheet.update_cell(17, 3, user.datetask)
    elif user.vehicle == "6 TON21837":
        sheet.update_cell(18, 3, user.datetask)
    elif user.vehicle == "6 TON21827":
        sheet.update_cell(19, 3, user.datetask)


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
    elif user.vehicle == "OUV34369":
        sheet.update_cell(8, 2, user.datetask)
    elif user.vehicle == "CBT AMB34827":
        sheet.update_cell(9, 2, user.datetask)
    elif user.vehicle == "CBT AMB34670":
        sheet.update_cell(10, 2, user.datetask)
    elif user.vehicle == "CBT AMB34770":
        sheet.update_cell(11, 2, user.datetask)
    elif user.vehicle == "6 TON21820":
        sheet.update_cell(12, 2, user.datetask)
    elif user.vehicle == "6 TON21948":
        sheet.update_cell(13, 2, user.datetask)
    elif user.vehicle == "6 TON21845":
        sheet.update_cell(14, 2, user.datetask)
    elif user.vehicle == "6 TON21817":
        sheet.update_cell(15, 2, user.datetask)
    elif user.vehicle == "6 TON21949":
        sheet.update_cell(16, 2, user.datetask)
    elif user.vehicle == "6 TON21814":
        sheet.update_cell(17, 2, user.datetask)
    elif user.vehicle == "6 TON21837":
        sheet.update_cell(18, 2, user.datetask)
    elif user.vehicle == "6 TON21827":
        sheet.update_cell(19, 2, user.datetask)

    updateBOCdate(vehicle)


@ bot.message_handler(commands=['remind'])
def scheduling(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add('05:30', '06:30', '07:30', '08:30', '09:30', '11:56')
    msg = bot.reply_to(
        message, "This function configures reminders timing. \n\nPlease enter your desired AM reminder time: ", reply_markup=markup)
    bot.register_next_step_handler(msg, process_amreminder_step)


def process_amreminder_step(message):
    try:
        chat_id = message.chat.id
        amreminder = message.text
        user = User(amreminder)
        user.amreminder = amreminder
        user_dict[chat_id] = user
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        markup.add('12:30', '13:30', '14:30',
                   '15:30', '16:30', '17:30', '11:33', '11:57')
        msg = bot.reply_to(
            message, 'Please enter your desired PM reminder time: ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_pmreminder_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


# cant work since heroku will not allow script to run forever
def process_pmreminder_step(message):
    try:
        chat_id = message.chat.id
        pmreminder = message.text
        user = user_dict[chat_id]
        user.pmreminder = pmreminder
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        markup.add('/remind')
        print(user.pmreminder)
        schedule.every().day.at("00:00").do(updatedate)
        schedule.every().day.at(user.amreminder).do(reminder)
        schedule.every().day.at(user.pmreminder).do(reminder)
        msg = bot.reply_to(
            message,  'Reminders configured\n\nAM: '+user.amreminder + '\nPM: ' + user.pmreminder + '\n\nTo reconfigure reminders, type \n/remind', reply_markup=markup)
        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
