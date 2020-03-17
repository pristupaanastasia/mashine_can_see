# -*- coding: utf-8 -*-

import telebot
import config_mysql
import user

TOKEN='895180391:AAHqS-rECfYK2Ibs0jEayVTn4xnH6psayac'

bot = telebot.TeleBot(TOKEN)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока', 'Создать мероприятие')

cnx = config_mysql.init_mysql()
cursor = cnx.cursor()

name_merop = ''
name = ''
user_id = -1
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
        sql = "INSERT INTO event(name, admin_tel_id) VALUES(%s, %s)"
        val = (str(name_merop), user_id)
        cursor.execute(sql, val)
        cnx.commit()
        add_event.add_event_json(cursor.lastrowid)
		bot.send_message(call.message.chat.id, 'Красавчик')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Пошел нахуй')

    
@bot.message_handler(content_types=['text'])
def send_text(message):
    global user_id
    if message.text.lower() == '1':
        bot.send_message(message.chat.id, 'Тест')
        sql = "Select * from events where id=1"
        cursor.execute(sql)
        res = cursor.fetchall()
        bot.send_message(message.chat.id, res[0][1])
    elif message.text.lower() == 'создать мероприятие':
        user_id = message.from_user.id
        bot.send_message(message.from_user.id, "Введите названия мероприятия:")
        bot.register_next_step_handler(message, get_name_mero)

@bot.message_handler(content_types=['photo'])
def send_photo(message):
    ids = user.get_photo(bot.get_file(message.photo[-1].file_id))
    print(ids)
    if ids != None:
    	sql = "Select info from users where id = " + str(ids[0])
    	cursor.execute(sql)
    	res = cursor.fetchall()
    	bot.send_message(message.chat.id, res[0])
    else:
        bot.send_message(message.chat.id, 'I dont know')    
    #bot.send_photo(message.chat.id, message.photo[-1].file_id)


def process_photo(message):
    photo = message.photo[-1].file_id
    message = bot.send_message('Имя и Фамилия')
    bot.register_next_step_handler(message, get_name)
def get_name(message):
    name = message.text()
	sql = "insert INTO users(info) VALUES ('"+str(name)+"')"
    cursor.execute(sql)
    res = cursor.fetchall()
    bot.send_message(message.chat.id, 'Мероприятие создано!')
 
bot.polling(none_stop=True, interval=0)
