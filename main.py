# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re

import telebot
import datetime, xlrd
import logging
logging.basicConfig(filename='example.log', level=logging.INFO)

bot = telebot.TeleBot('1615594110:AAGeoEWz34as6JKJMYVX4ZTLib7EBIBfscg')

rb = xlrd.open_workbook('test_serg.xls', formatting_info=True)
sheet = rb.sheet_by_index(0)
vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
range_valses = range(1, len(vals) - 1)
data = []
data.append("search")
for i in range_valses:
    data.append(vals[i][0] + " " + vals[i][1] + " " + vals[i][2] + " " + str(int(vals[i][5])))


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
                                                                         time=datetime.datetime.now(), m=message.text))        # if message.from_user.id == 283126393 or message.from_user.username == "natolich23":
        message_name = message.text.lower()
        message_name_added = ''
        for i in range(0, len(message_name)):
            if message_name[i] == '*' and i > 0:
                if message_name[i-1] != ' ':
                    message_name_added += ' '
            message_name_added += message_name[i]
            if message_name[i] == '*' and i < len(message_name) - 1:
                if message_name[i + 1] != ' ':
                    message_name_added += ' '
        message_name_added = re.sub(" +", " ", message_name_added)

        message_name_split = message_name_added.split(" ")
        count = 0
        while (len(message_name_split) < 4):
            message_name_split.append("*")
        first_found = 0
        regular = ''
        for i in range(0, len(message_name_split)):
            if message_name_split[i] == '*':
                first_found += 1
                regular += '\w+\s'
            else:
                regular += message_name_split[i] + '\s'
        is_all = True
        if first_found == 4:
            max = 0
            for i in range_valses:
                send_message_user(message, vals[i])
                max += 1
                if max == 10:
                    break
        else:
            for i in range_valses:
                if len(re.findall(regular, data[i].lower()+' ')) == 1:
                    count += 1
                    send_message_user(message, vals[i])
                # if count >= 10_000:
                if count >= 5:
                    is_all = False
                    break
            if count == 0:
                bot.send_message(message.chat.id, f'Не могу найти такого юзера')
            if not is_all:
                bot.send_message(message.chat.id, f'Выданны первые 5 записей, дополните критерии отбора')

    except Exception as e:
        bot.send_message(message.chat.id, f'Что-то пошло не так')


def send_message_user(message, val):
    bot.send_message(message.chat.id,
                     'Фамилия: {f} \nИмя: {n} \nОтчество: {s} \n\n{dob} \n\n{pof}'.format(f=val[0],
                                                                                          n=val[1],
                                                                                          s=val[2],
                                                                                          dob=datetime.datetime(
                                                                                              *xlrd.xldate_as_tuple(
                                                                                                  val[3],
                                                                                                  rb.datemode)).date().strftime(
                                                                                              "%d.%m.%Y"),
                                                                                          pof=val[4]))


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
