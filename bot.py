import pyodbc
from datetime import datetime
import re
from key import KEY_APY_TG, ADMIN_CHAT_ID

#conneсt database
try:
    con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=.\base\base.accdb;'
    conn = pyodbc.connect(con_string)
    print("Connected To Database")

except pyodbc.Error as e:
    print("Error in Connection database", e)

cur = conn.cursor()

#до когда действует подписка
def request_term(id_chat_user):
    request_date = 'SELECT * FROM base0 WHERE id_chat_user = ' + id_chat_user
    cur.execute(request_date)
    date_time = cur.fetchall()
    return(date_time[0][5].strftime("%d/%m/%y"))

#тариф
def request_rate(id_chat_user):
    request_rate_id = 'SELECT * FROM base0 WHERE id_chat_user = ' + id_chat_user
    cur.execute(request_rate_id)
    user_rate = cur.fetchall()
    user_rate_str = "'" + str(user_rate[0][4]) + "'"
    user_rate_data = 'SELECT * FROM Rate WHERE rate_kode = ' + user_rate_str
    cur.execute(user_rate_data)
    user_rate_return = cur.fetchall()
    return user_rate_return

#поиск юзера по ключу
def serch_user_sekure_key(secure_key):
     request_user_cekure = 'SELECT * FROM base0 WHERE pass_id = ' + secure_key
     cur.execute(request_user_cekure)
     user = cur.fetchall()
     if user:
        return user
     else:
        return False

#поиск юзера по чату
def serch_user_chat_id(id_chat):
     request_user_chat_id = 'SELECT * FROM base0 WHERE id_chat_user = ' + id_chat
     cur.execute(request_user_chat_id)
     user = cur.fetchall()
     if user:
        return True
     else:
        return False

#изменение чат id
def write_user_chat_id(user,chat_id):
    cur.execute('UPDATE base0 SET id_chat_user = ? WHERE user_key = ?', (chat_id, user))
    conn.commit()

# Михаил, хуярьте здесь хуйню всякую если что-то нужно поменять

HELLO_TEXT_NOIDENTITI="Привет, я тебя не знаю! Напиши мне свой код аудетификации, если нет обратись к админу или не преходи сюда больше"
HELLO_TEXT_IDE="Привет, рад тебя видеть"
MASSAGE_ADMIN = "пиши сучара почитаем https://t.me/TheSkoCh"
MASSAGE_REFUND = "честно бабки я тебе не очень хочу возвращать так что пиши сучара почитаем https://t.me/TheSkoCh"


import telebot
from telebot import types
bot = telebot.TeleBot(KEY_APY_TG)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if serch_user_chat_id("'" + str(message.from_user.id) + "'"):
        if message.text == "/start":
            bot.send_message(message.from_user.id, HELLO_TEXT_IDE)
        else:
            bot.send_message(message.from_user.id, "Тыт вошел но пишеш фигню вот те менюха")
            keyboard = types.InlineKeyboardMarkup()
            key_date_subscription = types.InlineKeyboardButton(text='до когда подписон', callback_data='key_date_subscription')
            keyboard.add(key_date_subscription)

            key_call_support = types.InlineKeyboardButton(text='поддержка', callback_data='key_call_support')
            keyboard.add(key_call_support)

            key_refund = types.InlineKeyboardButton(text='отмена подписки/возврат средств', callback_data='key_refund')
            keyboard.add(key_refund)

            key_payment = types.InlineKeyboardButton(text='купи говна ', callback_data='key_payment')
            keyboard.add(key_payment)

            question = 'Меню говна'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


    elif message.text[0:9] == "code_ide:":
        user = serch_user_sekure_key("'" + str(message.text) + "'")
        if user:
            write_user_chat_id(user[0][0],str(message.from_user.id))
            bot.send_message(message.from_user.id, "Ты вошел, добро пожаловать " + user[0][1])
        else:
            bot.send_message(message.from_user.id, "Код не верен")
    else:
        bot.send_message(message.from_user.id, HELLO_TEXT_NOIDENTITI)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "key_date_subscription":
        rate_farsh = request_rate ("'" + str(call.message.chat.id) + "'")[0]
        masage = "Подписка действует до " + str(request_term("'" + str(call.message.chat.id) + "'")) + "\n тариф блять: " + str(rate_farsh[1]) + "\n стоимость нахуй " + re.sub(r"\.\d+", "", str(rate_farsh[2])) + " p."
        bot.send_message(call.message.chat.id, masage)
        bot.answer_callback_query(call.id)
    elif call.data == "key_call_support":
        bot.send_message(call.message.chat.id, MASSAGE_ADMIN)
        bot.answer_callback_query(call.id)
    elif call.data == "key_refund":
        bot.send_message(call.message.chat.id, MASSAGE_REFUND)
        bot.answer_callback_query(call.id)
    elif call.data == "key_payment":
        bot.send_message(call.message.chat.id, "тут ветвление нахуячим")
        bot.answer_callback_query(call.id)




bot.polling(none_stop=True, interval=0)