
from telegram.ext import Updater, CommandHandler
# -*- coding: utf-8 -*-
import telebot
import time

TOKEN='895180391:AAHqS-rECfYK2Ibs0jEayVTn4xnH6psayac'
# REQUEST_KWARGS={
#     'proxy_url': 'https://185.36.191.39:5588',
#     # Optional, if you need authentication:
#     'urllib3_proxy_kwargs': {
#         'username': 'userid78DL',
#         'password': '2Hq829lQ',
#     }
# }

# updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)

bot = telebot.TeleBot(TOKEN)
#keyboard1 = telebot.types.ReplyKeyboardMarkup()
#keyboard1.row('Привет', 'Пока')
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == '1':
        bot.send_message(message.chat.id, 'Тест')
    elif message.text.lower() == '2':
        bot.send_message(message.chat.id, 'Тест2')
    elif message.text.lower() == '3':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')

@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)
bot.polling()
# from telebot import apihelper
# apihelper.proxy = {
    # 'https': 'socks5h://127.127.127.127:12345'
# }