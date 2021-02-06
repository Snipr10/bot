# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import telebot
import datetime
import logging
import csv

logging.basicConfig(filename='prod.log', level=logging.INFO)

bot = telebot.TeleBot('1615594110:AAGeoEWz34as6JKJMYVX4ZTLib7EBIBfscg')

state = []
first_name = []
last_name = []
second_name = []
DFB = []
Workplace = []
data = []
year = []
data_update = []


def delete_symbols(line):
    if line is not None:
        return re.sub('\[|]|\ |\'', '', line)


with open('prod.csv', newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        try:
            user = []
            data_split = (str(row)).split(",")
            this_DFB = delete_symbols(data_split[4])
            user.append(delete_symbols(data_split[1]))
            user.append(delete_symbols(data_split[2]))
            user.append(delete_symbols(data_split[3]))
            d_year = ""
            try:
                d_year = this_DFB.split('.')[2]
            except Exception:
                pass
            user.append(d_year)
            user.append(this_DFB)
            user.append(re.sub('\[|]|\'', '', data_split[5]))
            user.append(delete_symbols(data_split[0]))
            data.append(user)
        except Exception:
            print("Skip: " + str(row))

range_valses = range(1, len(data) - 1)
print("start")

white_list_username_search = ['bongiozzo', 'nikonovigor', 'kazarin', 'natolich23', 'oleggsh', 'segaunit',
                              'alexsandra7082',
                              'Spbvladimir',
                              'dmitry_11spb', 'ploxoeclovo', 'kupets78', 'iumironov93', 'profit878', 'dimmi_sh',
                              'MP_SPb',
                              'anebog', 'terekhovea', 'sashasashabyk', 'vadpa', 'deniskalm', 'lex8405',
                              'anna_kuznezova_11',
                              'mik_pro', 'alex14redtown', 'blackpirat3', 'simurden', 'operok', 'ragnar']
white_list_id_search = [283126393, 415757631]

white_list_username_logs = ['bongiozzo', 'oleggsh']
white_list_id_slogs = [283126393, 415757631]


def check_access_search(from_user):
    try:
        if from_user.id in white_list_id_search or from_user.username.lower() in white_list_username_search or from_user.username in white_list_username_search:
            return True
        return False
    except Exception:
        return False


def check_access_logs(from_user):
    try:
        if from_user.id in white_list_id_slogs or from_user.username.lower() in white_list_username_logs or from_user.username in white_list_username_logs:
            return True
        return False
    except Exception:
        return False


def add_logs(message):
    try:
        logging.info('used_id: {used_id} username: {username} time: {time} message: {m}'.format(used_id=message.from_user.id,
                                                                           username=message.from_user.username,
                                                                           time=datetime.datetime.now(),
                                                                           m=message.text))
    except Exception as e:
        print(e)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if check_access_search(message.from_user):
        bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')
    else:
        bot.reply_to(message, f'Нет доступа')
    add_logs(message)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    if check_access_search(message.from_user):
        bot.reply_to(message, f'Отправь мне фамилию, имя, отчество, дату рождения,  я верну данные')
    else:
        bot.reply_to(message, f'Нет доступа')
    add_logs(message)


@bot.message_handler(commands=['log'])
def send_welcome(message):
    if check_access_logs(message.from_user):
        try:
            f = open("prod.log", "rb")
            bot.send_document(message.chat.id, f)
        except Exception as e:
            bot.reply_to(message, f'Попробуй позже')
    else:
        bot.reply_to(message, f'Нет доступа')
    add_logs(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if check_access_search(message.from_user):
        try:
            message_name = message.text.lower()
            message_name_added = ''
            for i in range(0, len(message_name)):
                if message_name[i] == '*' and i > 0:
                    if message_name[i - 1] != ' ':
                        message_name_added += ' '
                message_name_added += message_name[i]
                if message_name[i] == '*' and i < len(message_name) - 1:
                    if message_name[i + 1] != ' ':
                        message_name_added += ' '
            message_name_added = re.sub(" +", " ", message_name_added)

            message_name_split = message_name_added.split(" ")
            while len(message_name_split) < 4:
                message_name_split.append("*")
            first_search = 0
            for datas in message_name_split:
                if datas == "*":
                    first_search += 1
                else:
                    break
            is_all = True
            count = 0

            if first_search == 4:
                for i in range_valses:
                    if count < 10:
                        send_message_user(message, i)
                        count += 1
            else:
                if first_search == 3:
                    first_message_data = 4
                else:
                    first_message_data = first_search
                for i in range_valses:
                    if data[i][first_message_data].lower() == message_name_split[first_search]:
                        check = True
                        for k in range(first_search, len(message_name_split)):
                            if message_name_split[k] != "*":
                                if k != 3 or len(message_name_split[k]) == 4:
                                    t = k
                                else:
                                    t = 4
                                if message_name_split[k] != data[i][t].lower():
                                    check = False
                        if check:
                            count += 1
                            send_message_user(message, i)
                    if count >= 5:
                        is_all = False
                        break
                if count == 0:
                    bot.send_message(message.chat.id, f'Не могу найти такого юзера')
                if not is_all:
                    bot.send_message(message.chat.id, f'Выданы первые 5 записей, дополните критерии отбора')

        except Exception as e:
            bot.send_message(message.chat.id, f'Что-то пошло не так')
    else:
        bot.reply_to(message, f'Нет доступа')
    add_logs(message)


def send_message_user(message, i):
    try:
        bot.send_message(message.chat.id,
                         'Фамилия: {f} \nИмя: {n} \nОтчество: {s} \nДата рождения: {dob} \nМесто работы: {pof} '
                         '\nРайон: {state}'.format(f=data[i][0],
                                                   n=data[i][1],
                                                   s=data[i][2],
                                                   dob=data[i][4],
                                                   pof=data[i][5],
                                                   state=data[i][6]))
    except Exception as e:
        print(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.polling(none_stop=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
