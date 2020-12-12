import gspread
import telebot
from telebot import types
from oauth2client.service_account import ServiceAccountCredentials
import time
import datetime
import schedule
from pprint import pprint


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open('Test Sheet').get_worksheet(0)


time1 = "06:00"  # to update by user
time2 = "12:00"  # to update by user
reminderdays = 5  # to update by user

# compares two days and returns the difference in number of days


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


def checkdate():
    i = 2
    while i < 9:
        days_to_jit = int(sheet.cell(i, 6).value)
        days_to_boc = int(sheet.cell(i, 7).value)
    # if days_to_jit <=reminderdays:
    # bot.send_message("You have %i days left till the next JIT deadline",days_to_jit)
    # if days_to_boc <=reminderdays:
    # bot.send_message("You have %i days left till the next BOC deadline",days_to_BOC)

# changed


def updateBOCdate(
        vehicle):  # updates the BOC date to current date when called, takes in vehicle string (as in first column of spreadsheet)
    currentdatestr = datetime.datetime.today().strftime(
        '%d/%m/%y')  # makes a datetime string to input into cell
    if vehicle == "MDTV41001":
        sheet.update_cell(2, 3, currentdatestr)
    elif vehicle == "MDTV41002":
        sheet.update_cell(3, 3, currentdatestr)
    elif vehicle == "MDTV41003":
        sheet.update_cell(4, 3, currentdatestr)
    elif vehicle == "MDTV41004":
        sheet.update_cell(5, 3, currentdatestr)
    elif vehicle == "MDTV41005":
        sheet.update_cell(6, 3, currentdatestr)
    elif vehicle == "OUV34375":
        sheet.update_cell(7, 3, currentdatestr)
    elif vehicle == "OUV33780":
        sheet.update_cell(8, 3, currentdatestr)
    elif vehicle == "CBT AMB34827":
        sheet.update_cell(9, 3, currentdatestr)
    elif vehicle == "CBT AMB34670":
        sheet.update_cell(10, 3, currentdatestr)
    elif vehicle == "CBT AMB34789":
        sheet.update_cell(11, 3, currentdatestr)
    elif vehicle == "6 TON21820":
        sheet.update_cell(12, 3, currentdatestr)
    elif vehicle == "6 TON21948":
        sheet.update_cell(13, 3, currentdatestr)
    elif vehicle == "6 TON21845":
        sheet.update_cell(14, 3, currentdatestr)
    elif vehicle == "6 TON21832":
        sheet.update_cell(15, 3, currentdatestr)
    elif vehicle == "6 TON21946":
        sheet.update_cell(16, 3, currentdatestr)
    elif vehicle == "6 TON21789":
        sheet.update_cell(17, 3, currentdatestr)
    elif vehicle == "6 TON21943":
        sheet.update_cell(18, 3, currentdatestr)
    elif vehicle == "6 TON21827":
        sheet.update_cell(19, 3, currentdatestr)


# updates JIT date to current date when called, takes in vehicle string (as in first column of spreadsheet)
def updateJITdate(vehicle):
    currentdatestr = datetime.datetime.today().strftime(
        '%d/%m/%y')  # makes a datetime string to input into cell
    if vehicle == "MDTV41001":
        sheet.update_cell(2, 2, currentdatestr)
    elif vehicle == "MDTV41002":
        sheet.update_cell(3, 2, currentdatestr)
    elif vehicle == "MDTV41003":
        sheet.update_cell(4, 2, currentdatestr)
    elif vehicle == "MDTV41004":
        sheet.update_cell(5, 2, currentdatestr)
    elif vehicle == "MDTV41005":
        sheet.update_cell(6, 2, currentdatestr)
    elif vehicle == "OUV34375":
        sheet.update_cell(7, 2, currentdatestr)
    elif vehicle == "OUV33780":
        sheet.update_cell(8, 2, currentdatestr)
    elif vehicle == "CBT AMB34827":
        sheet.update_cell(9, 2, currentdatestr)
    elif vehicle == "CBT AMB34670":
        sheet.update_cell(10, 2, currentdatestr)
    elif vehicle == "CBT AMB34789":
        sheet.update_cell(11, 2, currentdatestr)
    elif vehicle == "6 TON21820":
        sheet.update_cell(12, 2, currentdatestr)
    elif vehicle == "6 TON21948":
        sheet.update_cell(13, 2, currentdatestr)
    elif vehicle == "6 TON21845":
        sheet.update_cell(14, 2, currentdatestr)
    elif vehicle == "6 TON21832":
        sheet.update_cell(15, 2, currentdatestr)
    elif vehicle == "6 TON21946":
        sheet.update_cell(16, 2, currentdatestr)
    elif vehicle == "6 TON21789":
        sheet.update_cell(17, 2, currentdatestr)
    elif vehicle == "6 TON21943":
        sheet.update_cell(18, 2, currentdatestr)
    elif vehicle == "6 TON21827":
        sheet.update_cell(19, 2, currentdatestr)

    updateBOCdate(vehicle)
    updatedate()


# updates days left at the start of every day
schedule.every().day.at("00:00").do(updatedate)
# checks date and sends push message accordingly
schedule.every().day.at(time1).do(checkdate)
# checks date and sends push message accordingly
schedule.every().day.at(time2).do(checkdate)
