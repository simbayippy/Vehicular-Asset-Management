import telebot
from telebot import types
import time
import os
from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import requests
import schedule

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

server = Flask(__name__)
API_TOKEN = '1395353835:AAG2S0pc3uUL2oGbnQLBycnECAj_SqZv4uI'
bot = telebot.TeleBot(API_TOKEN)
user_dict = {}


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
            markup.add('39th', '40th', '41st')
            msg = bot.reply_to(
                message, "Enter your platoon: ", reply_markup=markup)
            bot.register_next_step_handler(msg, process_pre_platoon_step)
        else:
            markup.add('/start')
            msg = bot.reply_to(
                message, 'Incorrect passcode. Check with your PC/FS for the correct passcode. \n(passcode is case sensitive) \n\nPlease restart the bot by typing /start.', reply_markup=markup)
    except Exception as e:
        pass


def process_pre_platoon_step(message):
    try:
        chat_id = message.chat.id
        pre_platoon = message.text
        print('Users platoon: ' + pre_platoon)
        user = User(pre_platoon)
        user_dict[chat_id] = user
        user.pre_platoon = pre_platoon
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)

        if pre_platoon == '39th':
            markup.add('Sailesh', 'Gi Suk', 'Kian Siang', 'Abilash', 'Firdaus', 'Jeng Yi', 'Shariff', 'Ray', 'Jian Hao', 'Baodo', 'Ilyas', 'Mazlan', 'Ji Hao', 'Prithiv', 'Balaji', 'Elden',
                       'Sadiq', 'Ismail', 'Beaumont', 'Teng Hee', 'Kim', 'Zahid', 'Ramlan', 'Harith', 'Hamidi', 'Santhosh', 'Wei Tao', 'Farhan', 'Enzo', 'Syazwan', 'Idris', 'Perumal', 'Ezuan', 'Danish')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        elif pre_platoon == '40th':
            markup.add('Steven', 'Ethan', 'Rizwan', 'Anish', 'Kaiser', 'Zulfan', 'Qi Rui', 'Chen Jun', 'Josh', 'Asher', 'Simba', 'Abhi', 'Ming Ju', 'Sim Wei', 'Shinn', 'Kyaw Soe', 'Frederick', 'Ming Xuan',
                       'Cedric', 'Shannon', 'Min Hong', 'Darius', 'Sidharth', 'Jazz', 'Ranveer', 'Chao Ming', 'Abdiel', 'Royston', 'Kester', 'Wendell', 'Ryan', 'Paolo', 'Sibi', 'Benjamin', 'Ming Hui', 'William')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        elif pre_platoon == '41st':
            markup.add('no names yet')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_nameing_step)
    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


def process_nameing_step(message):
    try:
        chat_id = message.chat.id
        nameing = message.text
        user = user_dict[chat_id]
        user.nameing = nameing
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('Yes', 'No')
        msg = bot.reply_to(message,  'Please verify that the following information is *correct*\n\nYour platoon is: ' + user.pre_platoon +
                           '\nYour name is: ' + user.nameing, reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_verify_step)
    except Exception as e:
        pass


def process_verify_step(message):
    try:
        chat_id = message.chat.id
        verify = message.text
        user = user_dict[chat_id]
        user.verify = verify
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        print(user.pre_platoon)
        print(user.nameing)
        if verify == 'Yes':
            bot.send_message(
                chat_id, 'You have successfully been registered into our database. \n\nDo not delete/stop this bot in case of a recall. \n\nHave a nice day.')
            spreadsheet = client.open('sheets')
            sheet = spreadsheet.get_worksheet(3)

            # sheet.find needs to be in str
            chat_id = str(message.chat.id)
            try:
                # if user alr registered, will not add
                sheet.find(chat_id)
                print('user already present in database')
                pass
            except gspread.exceptions.CellNotFound:
                print('user not present in database, has now been added')
                user_id = [message.chat.id]
                # if user not registered, will add to database
                sheet.insert_row(user_id, 1)
                print(user_id)

            if user.pre_platoon == "39th":
                sheet = client.open('sheets').get_worksheet(0)
                if user.nameing == "simba":
                    sheet.update('B2:C2', [[user.time, user.location]])
            elif user.pre_platoon == "40th":
                sheet = client.open('sheets').get_worksheet(1)
                if user.nameing == 'Steven':
                    sheet.update_acell('D3', 'yes')
                elif user.nameing == 'Ethan':
                    sheet.update_acell('D4', 'yes')
                elif user.nameing == 'Rizwan':
                    sheet.update_acell('D7', 'yes')
                elif user.nameing == 'Anish':
                    sheet.update_acell('D8', 'yes')
                elif user.nameing == 'Kaiser':
                    sheet.update_acell('D9', 'yes')
                elif user.nameing == 'Zulfan':
                    sheet.update_acell('D10', 'yes')
                elif user.nameing == 'Qi Rui':
                    sheet.update_acell('D11', 'yes')
                elif user.nameing == 'Chen Jun':
                    sheet.update_acell('D12', 'yes')
                elif user.nameing == 'Josh':
                    sheet.update_acell('D13', 'yes')
                elif user.nameing == 'Asher':
                    sheet.update_acell('D14', 'yes')
                elif user.nameing == 'Simba':
                    sheet.update_acell('D15', 'yes')
                elif user.nameing == 'Abhi':
                    sheet.update_acell('D16', 'yes')
                elif user.nameing == 'Ming Jun':
                    sheet.update_acell('D19', 'yes')
                elif user.nameing == 'Sim Wei':
                    sheet.update_acell('D20', 'yes')
                elif user.nameing == 'Shinn':
                    sheet.update_acell('D21', 'yes')
                elif user.nameing == 'Kyaw Soe':
                    sheet.update_acell('D22', 'yes')
                elif user.nameing == 'Frederick':
                    sheet.update_acell('D23', 'yes')
                elif user.nameing == 'Ming Xuan':
                    sheet.update_acell('D24', 'yes')
                elif user.nameing == 'Cedric':
                    sheet.update_acell('D25', 'yes')
                elif user.nameing == 'Shannon':
                    sheet.update_acell('D26', 'yes')
                elif user.nameing == 'Min Hong':
                    sheet.update_acell('D29', 'yes')
                elif user.nameing == 'Darius':
                    sheet.update_acell('D30', 'yes')
                elif user.nameing == 'Jazz':
                    sheet.update_acell('D31', 'yes')
                elif user.nameing == 'Ranveer':
                    sheet.update_acell('D32', 'yes')
                elif user.nameing == 'Chao Ming':
                    sheet.update_acell('D33', 'yes')
                elif user.nameing == 'Abdiel':
                    sheet.update_acell('D36', 'yes')
                elif user.nameing == 'Royston':
                    sheet.update_acell('D37', 'yes')
                elif user.nameing == 'Kester':
                    sheet.update_acell('D38', 'yes')
                elif user.nameing == 'Wendell':
                    sheet.update_acell('D39', 'yes')
                elif user.nameing == 'Ryan':
                    sheet.update_acell('D40', 'yes')
                elif user.nameing == 'Paolo':
                    sheet.update_acell('D41', 'yes')
                elif user.nameing == 'Sibi':
                    sheet.update_acell('D42', 'yes')
                elif user.nameing == 'Benjamin':
                    sheet.update_acell('D43', 'yes')
                elif user.nameing == 'Ming Hui':
                    sheet.update_acell('D44', 'yes')
                elif user.nameing == 'William':
                    sheet.update_acell('D45', 'yes')
                elif user.nameing == '':
                    sheet.update_acell('D46', 'yes')
                else:
                    pass
            if user.pre_platoon == "41st":
                sheet = client.open('sheets').get_worksheet(2)
                if user.nameing == "no names yet":
                    sheet.update('B2:C2', [[user.time, user.location]])

        else:
            markup.add('/start')
            msg = bot.reply_to(
                message,  ' Please restart this form', reply_markup=markup)
    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/start')


@ bot.message_handler(commands=['acknowledged', 'submitanother', 'restart'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    markup.add('39th', '40th', '41st')
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

        if platoon == '39th':
            markup.add('Sailesh', 'Gi Suk', 'Kian Siang', 'Abilash', 'Firdaus', 'Jeng Yi', 'Shariff', 'Ray', 'Jian Hao', 'Baodo', 'Ilyas', 'Mazlan', 'Ji Hao', 'Prithiv', 'Balaji', 'Elden',
                       'Sadiq', 'Ismail', 'Beaumont', 'Teng Hee', 'Kim', 'Zahid', 'Ramlan', 'Harith', 'Hamidi', 'Santhosh', 'Wei Tao', 'Farhan', 'Enzo', 'Syazwan', 'Idris', 'Perumal', 'Ezuan', 'Danish')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        elif platoon == '40th':
            markup.add('Steven', 'Ethan', 'Rizwan', 'Anish', 'Kaiser', 'Zulfan', 'Qi Rui', 'Chen Jun', 'Josh', 'Asher', 'Simba', 'Abhi', 'Ming Ju', 'Sim Wei', 'Shinn', 'Kyaw Soe', 'Frederick', 'Ming Xuan',
                       'Cedric', 'Shannon', 'Min Hong', 'Darius', 'Sidharth', 'Jazz', 'Ranveer', 'Chao Ming', 'Abdiel', 'Royston', 'Kester', 'Wendell', 'Ryan', 'Paolo', 'Sibi', 'Benjamin', 'Ming Hui', 'William')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)
        elif platoon == '41st':
            markup.add('no names yet')
            msg = bot.reply_to(
                message, 'Enter your name:', reply_markup=markup)

        else:
            pass
        bot.register_next_step_handler(msg, process_naming_step)
    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/restart')


def process_naming_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = user_dict[chat_id]
        user.name = name
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('Yes', 'No')
        msg = bot.reply_to(message,  'Please verify that the following information is *correct*\n \nYour platoon is: ' + user.platoon +
                           '\nYour name is: ' + user.name, reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_verification_step)
    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/restart')


def process_verification_step(message):
    try:
        chat_id = message.chat.id
        verification = message.text
        print('Details correrct?: ' + verification)
        print(chat_id)
        markup = types.ReplyKeyboardMarkup(
            row_width=2, one_time_keyboard=True)
        if verification == 'Yes':
            spreadsheet = client.open('sheets')
            sheet = spreadsheet.get_worksheet(3)
            chat_id = str(message.chat.id)
            try:
                cell = sheet.find(chat_id)
                cell_address = "%s" % (cell.row)
                print(cell_address)
                cell_reformatted = int(cell_address)
                sheet.delete_rows(cell_reformatted)
            except Exception:
                pass

            markup.add('0-10mins', '10-20mins', '20-30mins', '30-40mins',
                       '40-50mins', '50-60mins', '60-70mins', '70-80mins')
            msg = bot.reply_to(
                message,  'What is ur ETA to Nee Soon Camp?', reply_markup=markup)
            bot.register_next_step_handler(msg, process_time_step)
        else:
            markup.add('/restart')
            msg = bot.reply_to(
                message,  'Please restart this form', reply_markup=markup)
    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/restart')


def process_time_step(message):
    try:
        chat_id = message.chat.id
        time = message.text
        user = user_dict[chat_id]
        user.time = time
        markup = types.ReplyKeyboardMarkup(
            row_width=2, one_time_keyboard=True)
        # no use as of now
        location_button = types.KeyboardButton(
            'Send location', request_location=True)
        # end
        markup.add('Home', 'OTW to camp', 'With family/friends',
                   'Others')
        msg = bot.reply_to(
            message,  'Please send your current location', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_location_step)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/restart')


@ bot.message_handler(commands=['resendLocation'])
def process_location_step(message):
    try:
        chat_id = message.chat.id
        location = message.text
        user = user_dict[chat_id]
        if location == 'Others':
            user.location = location
            msg = bot.reply_to(message, 'Please specify:')
            bot.register_next_step_handler(msg, process_others_step)
        elif location == '/resendLocation':
            user.location = location
            msg = bot.reply_to(message, 'Please specify:')
            bot.register_next_step_handler(msg, process_others_step)

        else:
            user.location = location
            markup = types.ReplyKeyboardMarkup(
                row_width=1, one_time_keyboard=True)
            markup.add('/confirmed')
            msg = bot.reply_to(
                message,  'To confirm your details, please type \n/confirmed', reply_markup=markup)
            bot.register_next_step_handler(msg, process_sheets)
            bot.register_next_step_handler(msg, platoon40)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/restart')


def process_others_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        location = message.text
        user.location = location
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('Yes', 'No')
        msg = bot.reply_to(
            message, 'Please verify that your location is ' + location, reply_markup=markup)
        bot.register_next_step_handler(msg, process_locationverification)

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/restart')


def process_locationverification(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    location_verification = message.text
    if location_verification == 'Yes':
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('/confirmed')
        msg = bot.reply_to(
            message,  'To confirm your details, please type \n/confirmed', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sheets)
        bot.register_next_step_handler(msg, platoon40)
    elif location_verification == 'No':
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add('/resendLocation')
        msg = bot.reply_to(
            message,  'Please resend your location ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_location_step)


def process_sheets(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        markup = types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        markup.add("/submitanother")
        msg = bot.reply_to(
            message,  'Thank you. \n\nReport back to NEE SOON CAMP immediately, do not rush. *Safety First*. \n\nTo submit another from, type \n/submitanother', reply_markup=markup, parse_mode='Markdown')

        if user.platoon == "39th":
            platoon39(message)
        elif user.platoon == "40th":
            platoon40(message)
        elif user.platoon == "41st":
            pass

    except Exception as e:
        bot.reply_to(
            message, 'Invalid Input, please restart by typing \n/restart')


@ bot.message_handler(commands=['send_recall'])
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
        if password == 'MRF@ADMIN':
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


def process_verifyrecall_step(message):
    try:
        chat_id = message.chat.id
        verifyrecall = message.text
        user = user_dict[chat_id]
        user.verifyrecall = verifyrecall
        markup = types.ReplyKeyboardMarkup(
            row_width=2, one_time_keyboard=True)
        spreadsheet = client.open('sheets')
        sheet = spreadsheet.get_worksheet(3)
        if verifyrecall == 'Yes':
            schedule.every(1).minute.do(
                sendtoallusers2).tag('sendall')

            msg = bot.reply_to(
                message,  'Recall sent.', reply_markup=markup)
            msg = bot.send_message(
                chat_id, "A list of troopers ETA will also be sent to _admin group_", parse_mode='Markdown')
            send_list()
            schedule.every(2).minutes.do(send_list).tag('list40th')
            bot.send_message(
                '-307260384', 'This list of Troopers ETA will be updated and sent every 2 minutes.\n\nTo stop the sending of ETA list, go to @MRF_Recall_bot and type \n/stop_send_list.',)
            while True:
                schedule.run_pending()
                time.sleep(1)

        else:
            markup.add('/send_recall')
            msg = bot.reply_to(
                message,  'Please restart this form.', reply_markup=markup)
    except Exception as e:
        pass


def send_list():
    sheet = client.open('sheets').get_worksheet(0)
    vall = sheet.get("A2:C44")
    vallnew = "\n".join(map(str, vall)).replace(
        '[', '').replace(']', '').replace("'", '')
    # if want each line 2 people, .replace('[', '   '])
    bot.send_message(
        '-307260384', '**39th ETA** \n(Name, ETA, Location) \n\n' + vallnew)
    sheet = client.open('sheets').get_worksheet(1)
    val = sheet.get("A2:C46")
    valnew = "\n".join(map(str, val)).replace(
        '[', '').replace(']', '').replace("'", '')
    # if want each line 2 people, .replace('[', '   '])
    bot.send_message(
        '-307260384', '**40th ETA** \n(Name, ETA, Location) \n\n' + valnew)


@ bot.message_handler(commands=['send_list'])
def job(message):
    bot.reply_to(
        message, "Troopers ETA list will be sent to: \n@ (MRF_recall_admin) group")
    send_list()


@ bot.message_handler(commands=['stop_send_list'])
def stop_send_list(message):
    bot.reply_to(
        message, "ETA list has stopped sending to admin group. \n\nHave a nice day")
    schedule.clear('list40th')


def sendtoallusers(message):
    spreadsheet = client.open('sheets')
    sheet = spreadsheet.get_worksheet(3)
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
    spreadsheet = client.open('sheets')
    sheet = spreadsheet.get_worksheet(3)
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


def platoon39(message):
    chat_id = message.chat.id
    sheet = client.open('sheets').get_worksheet(0)
    user = user_dict[chat_id]
    if user.name == "Sailesh":
        sheet.update('B3:C3', [[user.time, user.location]])
    elif user.name == "Gi Suk":
        sheet.update('B4:C4', [[user.time, user.location]])
    elif user.name == "Kian Siang":
        sheet.update('B7:C7', [[user.time, user.location]])
    elif user.name == "Abilash":
        sheet.update('B8:C8', [[user.time, user.location]])
    elif user.name == "Firdaus":
        sheet.update('B9:C9', [[user.time, user.location]])
    elif user.name == "Jeng Yi":
        sheet.update('B10:C10', [[user.time, user.location]])
    elif user.name == "Shariff":
        sheet.update('B11:C11', [[user.time, user.location]])
    elif user.name == "Ray":
        sheet.update('B12:C12', [[user.time, user.location]])
    elif user.name == "Jian Hao":
        sheet.update('B13:C13', [[user.time, user.location]])
    elif user.name == "Baodo":
        sheet.update('B14:C14', [[user.time, user.location]])
    elif user.name == "Ilyas":
        sheet.update('B15:C15', [[user.time, user.location]])
    elif user.name == "Mazlan":
        sheet.update('B16:C16', [[user.time, user.location]])
    elif user.name == "Ji Hao":
        sheet.update('B19:C19', [[user.time, user.location]])
    elif user.name == "Prithiv":
        sheet.update('B20:C20', [[user.time, user.location]])
    elif user.name == "Balaji":
        sheet.update('B21:C21', [[user.time, user.location]])
    elif user.name == "Elden":
        sheet.update('B22:C22', [[user.time, user.location]])
    elif user.name == "Sadiq":
        sheet.update('B23:C23', [[user.time, user.location]])
    elif user.name == "Ismail":
        sheet.update('B24:C24', [[user.time, user.location]])
    elif user.name == "Beaumont":
        sheet.update('B25:C25', [[user.time, user.location]])
    elif user.name == "Teng Hee":
        sheet.update('B26:C26', [[user.time, user.location]])
    elif user.name == "Kim":
        sheet.update('B29:C29', [[user.time, user.location]])
    elif user.name == "Zahid":
        sheet.update('B30:C30', [[user.time, user.location]])
    elif user.name == "Ramlan":
        sheet.update('B31:C31', [[user.time, user.location]])
    elif user.name == "Harith":
        sheet.update('B32:C32', [[user.time, user.location]])
    elif user.name == "Hamidi":
        sheet.update('B33:C33', [[user.time, user.location]])
    elif user.name == "Santhosh":
        sheet.update('B36:C36', [[user.time, user.location]])
    elif user.name == "Wei Tao":
        sheet.update('B37:C37', [[user.time, user.location]])
    elif user.name == "Farhan":
        sheet.update('B38:C38', [[user.time, user.location]])
    elif user.name == "Enzo":
        sheet.update('B39:C39', [[user.time, user.location]])
    elif user.name == "Syazwan":
        sheet.update('B40:C40', [[user.time, user.location]])
    elif user.name == "Idris":
        sheet.update('B41:C41', [[user.time, user.location]])
    elif user.name == "Perumal":
        sheet.update('B42:C42', [[user.time, user.location]])
    elif user.name == "Ezuan":
        sheet.update('B43:C42', [[user.time, user.location]])
    elif user.name == "Danish":
        sheet.update('B44:C44', [[user.time, user.location]])

    else:
        pass


def platoon40(message):
    chat_id = message.chat.id
    sheet = client.open('sheets').get_worksheet(1)
    user = user_dict[chat_id]
    if user.name == "Steven":
        sheet.update('B3:C3', [[user.time, user.location]])
    elif user.name == "Ethan":
        sheet.update('B4:C4', [[user.time, user.location]])
    elif user.name == "Rizwan":
        sheet.update('B7:C7', [[user.time, user.location]])
    elif user.name == "Anish":
        sheet.update('B8:C8', [[user.time, user.location]])
    elif user.name == "Kaiser":
        sheet.update('B9:C9', [[user.time, user.location]])
    elif user.name == "Zulfan":
        sheet.update('B10:C10', [[user.time, user.location]])
    elif user.name == "Qi Rui":
        sheet.update('B11:C11', [[user.time, user.location]])
    elif user.name == "Chen Jun":
        sheet.update('B12:C12', [[user.time, user.location]])
    elif user.name == "Josh":
        sheet.update('B13:C13', [[user.time, user.location]])
    elif user.name == "Asher":
        sheet.update('B14:C14', [[user.time, user.location]])
    elif user.name == "Simba":
        sheet.update('B15:C15', [[user.time, user.location]])
    elif user.name == "Abhi":
        sheet.update('B16:C16', [[user.time, user.location]])
    elif user.name == "Ming Jun":
        sheet.update('B19:C19', [[user.time, user.location]])
    elif user.name == "Sim Wei":
        sheet.update('B20:C20', [[user.time, user.location]])
    elif user.name == "Shinn":
        sheet.update('B21:C21', [[user.time, user.location]])
    elif user.name == "Kyaw Soe":
        sheet.update('B22:C22', [[user.time, user.location]])
    elif user.name == "Frederick":
        sheet.update('B23:C23', [[user.time, user.location]])
    elif user.name == "Ming Xuan":
        sheet.update('B24:C24', [[user.time, user.location]])
    elif user.name == "Cedric":
        sheet.update('B25:C25', [[user.time, user.location]])
    elif user.name == "Shannon":
        sheet.update('B26:C26', [[user.time, user.location]])
    elif user.name == "Min Hong":
        sheet.update('B29:C29', [[user.time, user.location]])
    elif user.name == "Darius":
        sheet.update('B30:C30', [[user.time, user.location]])
    elif user.name == "Sidharth":
        sheet.update('B31:C31', [[user.time, user.location]])
    elif user.name == "Jazz":
        sheet.update('B32:C32', [[user.time, user.location]])
    elif user.name == "Ranveer":
        sheet.update('B33:C33', [[user.time, user.location]])
    elif user.name == "Chao Ming":
        sheet.update('B36:C36', [[user.time, user.location]])
    elif user.name == "Abdiel":
        sheet.update('B37:C37', [[user.time, user.location]])
    elif user.name == "Royston":
        sheet.update('B38:C38', [[user.time, user.location]])
    elif user.name == "Kester":
        sheet.update('B39:C39', [[user.time, user.location]])
    elif user.name == "Wendell":
        sheet.update('B40:C40', [[user.time, user.location]])
    elif user.name == "Ryan":
        sheet.update('B41:C41', [[user.time, user.location]])
    elif user.name == "Paolo":
        sheet.update('B42:C42', [[user.time, user.location]])
    elif user.name == "Sibi":
        sheet.update('B43:C42', [[user.time, user.location]])
    elif user.name == "Benjamin":
        sheet.update('B44:C44', [[user.time, user.location]])
    elif user.name == "Ming Hui":
        sheet.update('B45:C45', [[user.time, user.location]])
    elif user.name == "William":
        sheet.update('B46:C46', [[user.time, user.location]])
    else:
        pass


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
