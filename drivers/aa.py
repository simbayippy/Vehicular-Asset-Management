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
API_TOKEN = '1364940659:AAHaEM0tWAxElCMy08zduOnC5cWd9vB4eP8'
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
        user_name = message.chat.first_name
        user.name = user_name
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
            row_width=2, one_time_keyboard=True)
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.datetask = datetask
        if len(datetask) == 8:
            markup.add('Full', '>3/4', '1/2 to 3/4', '<1/2')
            msg = bot.reply_to(
                message, 'What is the fuel level: \n\nDo remember to fill up if fuel level is low', reply_markup=markup)

            bot.register_next_step_handler(msg, process_fuel_step)

        else:
            markup.add('/resenddate')
            msg = bot.reply_to(
                message, 'Date has to be in the form \nDD/MM/YY. To re enter date, type \n/resenddate.', reply_markup=markup)
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
        elif user.vehicle == "MDTV41002":
            current_hoto = sheet.acell('I3').value
        elif user.vehicle == "MDTV41003":
            current_hoto = sheet.acell('I4').value
        elif user.vehicle == "MDTV41004":
            current_hoto = sheet.acell('I5').value
        elif user.vehicle == "MDTV41005":
            current_hoto = sheet.acell('I6').value
        elif user.vehicle == "OUV34375":
            current_hoto = sheet.acell('I7').value
        elif user.vehicle == "OUV33780":
            current_hoto = sheet.acell('I8').value
        elif user.vehicle == "CBT AMB34827":
            current_hoto = sheet.acell('I9').value
        elif user.vehicle == "CBT AMB34670":
            current_hoto = sheet.acell('I10').value
        elif user.vehicle == "CBT AMB34789":
            current_hoto = sheet.acell('I11').value
        elif user.vehicle == "6 TON21820":
            current_hoto = sheet.acell('I12').value
        elif user.vehicle == "6 TON21948":
            current_hoto = sheet.acell('I13').value
        elif user.vehicle == "6 TON21845":
            current_hoto = sheet.acell('I14').value
        elif user.vehicle == "6 TON21832":
            current_hoto = sheet.acell('I15').value
        elif user.vehicle == "6 TON21946":
            current_hoto = sheet.acell('I16').value
        elif user.vehicle == "6 TON21789":
            current_hoto = sheet.acell('I17').value
        elif user.vehicle == "6 TON21943":
            current_hoto = sheet.acell('I18').value
        elif user.vehicle == "6 TON21827":
            current_hoto = sheet.acell('I19').value

        markup.add('No issues', 'Issue has been expressed before')
        msg = bot.reply_to(
            message, 'Any vehicle issues to HOTO: \n\nCurrent status: ' + current_hoto + '\n\nIf there are any issues, please manually type in using your keyboard. \ne.g. dented left front tyre guard', reply_markup=markup)

        bot.register_next_step_handler(msg, process_HOTO_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, pleasee restart by typing \n/start')


def process_HOTO_step(message):
    hoto = message.text
    markup = types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True)
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.hoto = hoto
    if hoto == 'Issue has been expressed before':
        pass
    else:
        updatehoto(message)

    markup.add('Yes', 'No')
    msg = bot.reply_to(message,  'Please verify that the following information is correct\n\nYour vehicle is: ' + user.vtype + '\nVehicle number is: ' +
                       user.vnum + '\n\nTask is: ' + user.task + '\nDate of ' + user.task + ' : ' + user.datetask + '\nFuel level: ' + user.fuel + '\n\nIssue(s): ' + user.hoto, reply_markup=markup)

    bot.register_next_step_handler(msg, process_verify_step)


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
                chat_id, 'Input finished. To submit another, type \n/submitanother', reply_markup=markup)
            send_task_done(message)
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


def updatehoto(vehicle):
    chat_id = vehicle.chat.id
    user = user_dict[chat_id]
    if user.vehicle == "MDTV41001":
        sheet.update_cell(2, 9, user.hoto)
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


@bot.message_handler(commands=['sendreminder'])
def reminder(message):
    msg = bot.reply_to(
        message, "Actions to be taken will be sent to admin group")
    i = 2
    while i < 20:
        # jit
        days_to_jit = int(sheet.cell(i, 7).value)
        vnojit = sheet.cell(i, 1).value
        # boc
        days_to_boc = int(sheet.cell(i, 8).value)
        vnoboc = sheet.cell(i, 1).value
        # combined
        if days_to_jit <= reminderdays or days_to_boc <= reminderdays:
            bot.send_message(-490206159,
                             "_" + vnojit + "_  has " + str(days_to_jit) + " days left till the next JIT deadline \n" + "_" + vnoboc + "_  has " + str(days_to_boc) + " days left till the next BOC deadline")
        i += 1
    print('done')
    bot.send_message(-490206159, "hi")


def abc():
    i = 2
    while i < 20:
        # jit
        days_to_jit = int(sheet.cell(i, 7).value)
        vnojit = sheet.cell(i, 1).value
        # boc
        days_to_boc = int(sheet.cell(i, 8).value)
        vnoboc = sheet.cell(i, 1).value
        # combined
        if days_to_jit <= reminderdays or days_to_boc <= reminderdays:
            bot.send_message(-490206159,
                             "_" + vnojit + "_  has " + str(days_to_jit) + " days left till the next JIT deadline \n" + "_" + vnoboc + "_  has " + str(days_to_boc) + " days left till the next BOC deadline")
        i += 1
    print('done')


def checkdate():
    sheet = client.open('Test Sheet').get_worksheet(0)
    values = sheet.get("F2:H19")
    valuenew = "\n".join(map(str, values)).replace(
        '[', '').replace(']', '').replace("'", '')
    # if want each line 2 people, .replace('[', '   '])
    bot.send_message(
        '-490206159', '**Vehicle Maintanence** \n(Vc, days to JIT, days to BOC) \n\n' + valuenew)


@bot.message_handler(commands=['updateops'])
def updateops(message):
    sheet = client.open('Test Sheet').get_worksheet(0)
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    markup.add('MDTV', 'OUV', 'CBT AMB', '6 TON')
    msg = bot.reply_to(
        message, "Select vehicle type", reply_markup=markup)
    bot.register_next_step_handler(msg, process_ops)


def process_ops(message):
    try:
        chat_id = message.chat.id
        vops = message.text
        print('Vehicle Type: ' + vops)
        user = User(vops)
        user_dict[chat_id] = user
        user.vops = vops
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        if vops == 'MDTV':
            markup.add('41001', '41002', '41003', '41004', '41005')
            msg = bot.reply_to(
                message, 'Enter Vehicle that is mso 1:', reply_markup=markup)

        elif vops == 'OUV':
            markup.add('34375', '33780')
            msg = bot.reply_to(
                message, 'Enter Vehicle number:', reply_markup=markup)

        elif vops == 'CBT AMB':
            markup.add('34827', '34670', '34789')
            msg = bot.reply_to(
                message, 'Enter Vehicle number:', reply_markup=markup)

        elif vops == '6 TON':
            markup.add('21820', '21948', '21845', '21832',
                       '21946', '21789', '21943', '21827')
            msg = bot.reply_to(
                message, 'Enter Vehicle number:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_vno)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


def process_vno(message):
    try:
        chat_id = message.chat.id
        vno = message.text
        user = user_dict[chat_id]
        user.vnum = vno
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        if user.vops == 'MDTV':
            if vno == '41001':
                sheet.update_acell('A28', 'MSO1 41001')
                sheet.update_acell('A29', 'Spare 41002')
                sheet.update_acell('A30', 'Spare 41003')
                sheet.update_acell('A31', 'Spare 41004')
                sheet.update_acell('A32', 'Spare 41005')
            elif vno == '41002':
                sheet.update_acell('A28', 'Spare 41001')
                sheet.update_acell('A29', 'MSO1 41002')
                sheet.update_acell('A30', 'Spare 41003')
                sheet.update_acell('A31', 'Spare 41004')
                sheet.update_acell('A32', 'Spare 41005')
            elif vno == '41003':
                sheet.update_acell('A29', 'Spare 41001')
                sheet.update_acell('A28', 'Spare 41002')
                sheet.update_acell('A30', 'MSO1 41003')
                sheet.update_acell('A31', 'Spare 41004')
                sheet.update_acell('A32', 'Spare 41005')
            elif vno == '41004':
                sheet.update_acell('A29', 'Spare 41001')
                sheet.update_acell('A28', 'Spare 41002')
                sheet.update_acell('A30', 'Spare 41003')
                sheet.update_acell('A31', 'MSO1 41004')
                sheet.update_acell('A32', 'Spare 41005')
            elif vno == '41005':
                sheet.update_acell('A29', 'Spare 41001')
                sheet.update_acell('A28', 'Spare 41002')
                sheet.update_acell('A30', 'Spare 41003')
                sheet.update_acell('A31', 'Spare 41004')
                sheet.update_acell('A32', 'MSO1 41005')
                verifylist = sheet.get('A28:A32')
        sheet = client.open('Test Sheet').get_worksheet(0)
        verifylist = sheet.get("A28:A51")
        markup.add('Yes', 'No')
        msg = bot.reply_to(
            message,  'Please verify that the following information is correct\n\nUpdated vehicle list is\n' + verifylist, reply_markup=markup)
        bot.register_next_step_handler(msg, process_list)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


def process_list(message):
    try:
        listt = message.text
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.listt = listt
        verifylist = sheet.get('A28:A32')
        markup.add('Yes', 'No')
        msg = bot.reply_to(
            message,  'Please verify that the following information is correct\n\nUpdated vehicle list is\n' + verifylist, reply_markup=markup)

        bot.register_next_step_handler(msg, process_verify_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


def send_task_done(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    bot.send_message(-490206159, emoji.emojize(':minibus: :x:Vehicle type/number: ' + user.vtype + '/' + user.vnum + '\n:white_check_mark: Task done: ' + user.task +
                                               '\n:clock4: Date of ' + user.task + ' is: ' + user.datetask + '\n\nTask completed by: ' + user.name))


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
        markup = types.ReplyKeyboardMarkup(
            row_width=2, one_time_keyboard=True)
        markup.add('12:30', '13:30', '14:30',
                   '15:30', '16:30', '17:30', '11:33', '11:57')
        msg = bot.reply_to(
            message, 'Please enter your desired PM reminder time: ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_pmreminder_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


def process_pmreminder_step(message):
    try:
        chat_id = message.chat.id
        pmreminder = message.text
        user = user_dict[chat_id]
        user.pmreminder = pmreminder
        markup = types.ReplyKeyboardMarkup(
            row_width=2, one_time_keyboard=True)
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


bot.polling()
