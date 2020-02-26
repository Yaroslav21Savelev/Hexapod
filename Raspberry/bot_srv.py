#!/usr/bin/env python3.7

import telebot
from telebot import types
import cv2 as cv
import time
from datetime import datetime
capturing = False
cap = cv.VideoCapture(0)
bot = telebot.TeleBot('1005601952:AAGVqDe0LoKtHUs9xIgRvvzxKugcbzwr6zI')
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    b_all = types.KeyboardButton(
        text="Отправь все!")
    b_dell = types.KeyboardButton(
        text="Удали все!")
    keyboard.add(b_all)
    keyboard.add(b_dell)
    bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=keyboard)




@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    global capturing
    if message.text == "Отправь все!":
        try:
            import os
            directory = r'/home/pi/faces/'
            for entry in os.scandir(directory):
                if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():
                    print(entry.path)
                    bot.send_message(message.chat.id, entry.path)
                    bot.send_photo(message.chat.id, open(entry.path, 'rb'))
        except:
            bot.send_message(message.chat.id, "err")
    elif message.text == "Удали все!":
        try:
            import os
            directory = r'/home/pi/faces/'
            msg = "DELETED:\n"
            for entry in os.scandir(directory):
                if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():
                    msg += entry.path + "\n"
                    print(entry.path)
                    os.remove(entry.path)
            bot.send_message(message.chat.id, msg)
        except:
            bot.send_message(message.chat.id, "err")
    else:
        bot.send_message(message.chat.id, "Ошибка!")


# 637154599
from time import sleep
while True:
    try:
        bot.polling(none_stop=True)
    except:
        pass
