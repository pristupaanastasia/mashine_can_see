# -*- coding: utf-8 -*-

import telebot
import config_mysql

TOKEN='895180391:AAHqS-rECfYK2Ibs0jEayVTn4xnH6psayac'

bot = telebot.TeleBot(TOKEN)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока', 'Создать мероприятие')

cnx = config_mysql.init_mysql()
cursor = cnx.cursor()

name_merop = ''
name = ''
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /s2tart', reply_markup=keyboard1)

def get_name_mero(message):
    global name_merop
    name_merop = message.text
    key = telebot.types.InlineKeyboardMarkup()
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')
    key.add(key_yes)
    key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
    key.add(key_no)
    question = 'Вы действительно хотите создать мероприятие " ' + str(name_merop) + '"?'
    bot.send_message(message.from_user.id, text=question, reply_markup=key)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        sql = "Select * from event where name = '" + str(name_merop) + "'"
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) == 0:
            sql = "INSERT INTO event(name) VALUES('"+str(name_merop)+"')"
            cursor.execute(sql)
            cnx.commit()
            msq = bot.reply_to(call, 'фото')
			bot.register_next_step_handler(msq, process_photo)
        else:
           bot.send_message(call.message.chat.id, 'Такое мероприятие уже существует') 
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Пошел нахуй')

    
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == '1':
        bot.send_message(message.chat.id, 'Тест')
    elif message.text.lower() == 'создать мероприятие':
        bot.send_message(message.from_user.id, "Введите названия мероприятия:")
        bot.register_next_step_handler(message, get_name_mero)
    elif message.text.lower() == '2':
        bot.send_message(message.chat.id, 'Тест2')
    elif message.text.lower() == '3':
        bot.send_message(message.chat_id, 'makson blyat')

#@bot.message_handler(content_types=['photo'])
#def send_photo(message):
    #bot.send_photo(message.chat.id, message.photo[-1].file_id)
#    bot.send_message(message.chat.id, 'kek')

def process_photo(message):
    photo = message.photo[-1].file_id
    ld = bot.reply_to(message,'Имя и Фамилия')
    bot.register_next_step_handler(ld, get_name)
def get_name(message):
    name = message.text()
	sql = "INSERT INTO users(info) VALUES ('"+str(name)+"')"
    bot.send_message(message.chat.id, 'Мероприятие создано!')
 
bot.polling(none_stop=True, interval=0)
