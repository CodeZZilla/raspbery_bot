import os
import string
import random
from telebot.types import ReplyKeyboardMarkup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import telebot
import re
# import RPi.GPIO as GPIO
from time import sleep

red_led_pin = 21
green_led_pin = 20
button_pin = 16

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(red_led_pin, GPIO.OUT)
# GPIO.setup(green_led_pin, GPIO.OUT)
# GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


bot = telebot.TeleBot('1076743317:AAFAeIvVLM560ny-INNL6Iy3dn3L4Jm9jkk')
sticker_start = 'CAACAgUAAxkBAAP-X0qNH1rpyoDqT7odr43p9nZntwkAAm8DAALpCsgDr86-2QK6XXQbBA'

count_users = 0


def reply(id, message):
    vip_id = file_reader("id/vip_id.txt", "\n")
    if vip_id.__contains__(id):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('Інформація', "Відкрити двері")
        keyboard.row("Подивитися паролі")
        keyboard.row("Добавити адміністратора")
        keyboard.max_row_keys = 4
        print('Received:', message)
        now = datetime.datetime.now()
        if message.lower() == 'інформація':
            os.system('vcgencmd measure_temp > /home/pi/raspberry_bot/id/bot')
            with open('id/bot', 'r') as file:
                temp = file.read()
                bot.send_message(id, temp + 'Час: ' + str(now.hour) + ':' + str(now.minute) + ':' + str(
                    now.second) + '\n' + 'Дата: ' + str(now.day) + '/' + str(now.month) + str('/') + str(now.year),
                                 reply_markup=keyboard)
        elif message.lower() == 'відкрити двері':
            bot.send_message(id, 'Відкрито...', reply_markup=keyboard)
            # GPIO.output(red_led_pin, True)
            sleep(2)
            # GPIO.output(red_led_pin, False)
            bot.send_message(id, 'Зачинено!', reply_markup=keyboard)
        elif message.lower() == 'подивитися паролі':
            passwords = file_reader("id/pass.txt", "#*#")
            bot.send_message(id, "\n".join(passwords))
        elif message.lower() == "добавити адміністратора":
            user_id = file_reader("id/id.txt", "\n")
            s = ""
            num = 1
            for i in user_id:
                if(str(i) == ""):
                    break
                else:
                    s += str(num) + ". " + str(i) + "\n"
                    num += 1
            j = 1
            inline_keboard = InlineKeyboardMarkup()
            while j < num:
                data = "data" + str(j)
                but1 = InlineKeyboardButton(text=str(j), callback_data=data)
                inline_keboard.add(but1)
                j += 1
            global count_users
            count_users = num - 1
            bot.send_message(id, s, reply_markup=inline_keboard)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('Інформація', "Відкрити двері")
        print('Received:', message)
        now = datetime.datetime.now()
        if message.lower() == 'інформація':
            os.system('vcgencmd measure_temp > /home/pi/raspberry_bot/id/bot')
            with open('id/bot', 'r') as file:
                temp = file.read()
                bot.send_message(id, temp + 'Час: ' + str(now.hour) + ':' + str(now.minute) + ':' + str(
                    now.second) + '\n' + 'Дата: ' + str(now.day) + '/' + str(now.month) + str('/') + str(now.year),
                                 reply_markup=keyboard)
        elif message.lower() == 'відкрити двері':
            bot.send_message(id, 'Відкрито...', reply_markup=keyboard)
            # GPIO.output(red_led_pin, True)
            sleep(2)
            # GPIO.output(red_led_pin, False)
            bot.send_message(id, 'Зачинено!', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        data = re.findall('(\d+)', str(call.data))
        print(data)
        users = file_reader("id/id.txt", "\n")
        id = re.findall('^\S+', users[int(data[0]) - 1])

        id_vip = file_reader("id/vip_id.txt", "\n")

        if not id_vip.__contains__(str(id[0])):
            with open("id/vip_id.txt", "a") as file:
                file.write(str(id[0]) + "\n")
            bot.send_message(chat_id=call.message.chat.id, text=str(id[0]) + " - добавлено!")
        else:
            bot.send_message(chat_id=call.message.chat.id, text="oops!")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Введіть пароль:")
    id_not_checked = file_reader("id/no_cheked_id.txt", "\n")
    if not set(id_not_checked).__contains__(message.chat.id):
        id_not_checked.append(str(message.chat.id))
        id_temp = set(id_not_checked)
        with open("id/no_cheked_id.txt", "w") as file:
            file.write("")
        with open("id/no_cheked_id.txt", "a") as file:
            for item in id_temp:
                file.write(item + "\n")

@bot.message_handler(content_types=['text'])
def send_text(message):
    chat_id = str(message.chat.id)
    mes = message.text
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username_ = message.from_user.username
    id_cheked = file_reader("id/id.txt", "\n")
    id_not_cheked = file_reader("id/no_cheked_id.txt", "\n")
    print(id_cheked)
    print(id_not_cheked)
    print(chat_id)
    if id_not_cheked.__contains__(chat_id):
        pas_temp = file_reader("id/pass.txt", "#*#")
        if pas_temp.__contains__(mes):
            id_not_cheked.remove(str(chat_id))
            with open("id/no_cheked_id.txt", "w") as file:
                file.write("")
            with open("id/no_cheked_id.txt", "a") as file:
                for item in id_not_cheked:
                    file.write(item + "\n")
            file_pass(mes)
            id_append(chat_id, first_name, last_name, username_)
            bot.send_sticker(message.chat.id, sticker_start)
            bot.send_message(message.chat.id, 'Ласкаво просимо\nCodezilla bot')
            reply(chat_id, mes)
        else:
            bot.send_message(chat_id, "вибачте")
    elif not id_not_cheked.__contains__(chat_id):
        for i in id_cheked:
            if i.__contains__(chat_id):
                reply(chat_id, mes)
    else:
        bot.send_message(chat_id, "No access")

def id_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_file10():
    with open("id/pass.txt", "a") as file:
        for i in range(1, 4):
            file.write(id_generator() + "#*#")

def file_pass(password):
    passArr = file_reader("id/pass.txt", "#*#")
    passArr.remove(password)
    passArr.remove("")
    print(passArr)
    if passArr.__len__()==0:
        with open("id/pass.txt", "w") as file:
            file.write("")
        generate_file10()
    else:
        with open("id/pass.txt", "w") as file:
            file.write("")
        with open("id/pass.txt", "a") as file:
            for item in passArr:
                file.write(item + "#*#")

def id_cheker(id_user):
    users_id = file_reader("id/id.txt", "\n")
    if users_id.__contains__(str(id_user)):
        return True
    else:
        return False

def id_append(id_user, first_name, last_name, username):
    users = file_reader("id/id.txt", "\n")
    while True:
        if users.__contains__(""):
            users.remove("")
        else:
            break
    if not users.__contains__(str(id_user) + " " + str(first_name) + " " + str(last_name) + " " + str(username)):
        users.append(str(id_user) + " " + str(first_name) + " " + str(last_name) + " " + str(username))
        with open("id/id.txt", "w") as file:
            file.write("")
        with open("id/id.txt", "a") as file:
            for item in users:
                file.write(item + "\n")

def file_reader(path, split):
    arr = []
    with open(path, "r") as file:
        arr = file.read().split(split)
    return arr

print(bot.get_me())
print('Listening....')
bot.polling()
