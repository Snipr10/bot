# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re

import telebot
import datetime, xlrd
import logging

logging.basicConfig(filename='example.log', level=logging.INFO)

bot = telebot.TeleBot('1615594110:AAGeoEWz34as6JKJMYVX4ZTLib7EBIBfscg')
import csv

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


with open('test.csv', newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        user = []
        data_split = (str(row)).split(",")
        this_state = delete_symbols(data_split[0])
        this_first_name = delete_symbols(data_split[1])
        this_last_name = delete_symbols(data_split[2])
        this_second_name = delete_symbols(data_split[3])
        this_DFB = delete_symbols(data_split[4])
        this_Workplace = re.sub('\[|]|\'', '', data_split[5])
        user.append(this_first_name)
        user.append(this_last_name)
        user.append(this_second_name)
        d_year = ""
        try:
            d_year = this_DFB.split('.')[2]
        except Exception:
            pass
        user.append(d_year)
        user.append(this_DFB)
        user.append(this_Workplace)
        user.append(this_state)
        data.append(user)

range_valses = range(1, len(data) - 1)
print("start")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # if message.from_user.id == 283126393:
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')


@bot.message_handler(commands=['help'])
def send_welcome(message):
    # if message.from_user.id == 283126393:
    bot.reply_to(message, f'Отправь мне фамилию, я верну данные')


@bot.message_handler(commands=['log'])
def send_welcome(message):
    if message.from_user.username == 'bongiozzo' or message.from_user.username == 'oleggsh':
        try:
            f = open("example.log", "rb")
            bot.send_document(message.chat.id, f)
        except Exception as e:
            bot.reply_to(message, f'Попробуй позже')
    else:
        bot.reply_to(message, f'Нет доступа')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        logging.info('usedid: {usedid} time: {time} message: {m}'.format(usedid=message.from_user.id,
                                                                         time=datetime.datetime.now(),
                                                                         m=message.text))  # if message.from_user.id == 283126393 or message.from_user.username == "natolich23":
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
        while (len(message_name_split) < 4):
            message_name_split.append("*")
        first = 0
        for datas in message_name_split:
            if datas == "*":
                first += 1
            else:
                break
        is_all = True
        count = 0

        if first == 4:
            for i in range_valses:
                if count < 10:
                    send_message_user(message, i)
                    count += 1
        else:
            for i in range_valses:
                if data[i][first].lower() == message_name_split[first]:
                    check = True
                    for k in range(first, len(message_name_split)):
                        if message_name_split[k] != "*" and message_name_split[k] != data[i][k].lower():
                            check = False
                    if check:
                        count += 1
                        send_message_user(message, i)
                # if count >= 10_000:
                if count >= 5:
                    is_all = False
                    break
            if count == 0:
                bot.send_message(message.chat.id, f'Не могу найти такого юзера')
            if not is_all:
                bot.send_message(message.chat.id, f'Выданы первые 5 записей, дополните критерии отбора')

    except Exception as e:
        bot.send_message(message.chat.id, f'Что-то пошло не так')


def send_message_user(message, i):
    try:
        bot.send_message(message.chat.id,
                         'Фамилия: {f} \nИмя: {n} \nОтчество: {s} \nДата рождения: {dob} \nМесто работы: {pof} \nРайон: {state}'.format(f=data[i][0],
                                                                                                          n=data[i][1],
                                                                                                          s=data[i][2],
                                                                                                          dob=data[i][4],
                                                                                                          pof=data[i][5],
                                                                                                          state=data[i][6]))
    except Exception as e:
        print(e)

def print_hi(name):
    # открываем файл

    # выбираем активный лист
    sheet = rb.sheet_by_index(0)
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.polling(none_stop=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
