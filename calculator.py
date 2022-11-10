
# готовый калькулятор

import telebot


bot = telebot.TeleBot("5605526481:AAG9tx5MzA09nYUkPHA8Z_zkPtrpzmdg42M")
value = ''
old_value = ''
item = {}
keyboard = telebot.types.InlineKeyboardMarkup()

keyboard.row(telebot.types.InlineKeyboardButton('', callback_data='no'),
             telebot.types.InlineKeyboardButton('c', callback_data='c'),
             telebot.types.InlineKeyboardButton('<=', callback_data='<='),
             telebot.types.InlineKeyboardButton('/', callback_data='/'))

keyboard.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
             telebot.types.InlineKeyboardButton('8', callback_data='8'),
             telebot.types.InlineKeyboardButton('9', callback_data='9'),
             telebot.types.InlineKeyboardButton('*', callback_data='*'))

keyboard.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
             telebot.types.InlineKeyboardButton('5', callback_data='5'),
             telebot.types.InlineKeyboardButton('6', callback_data='6'),
             telebot.types.InlineKeyboardButton('-', callback_data='-'))

keyboard.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
             telebot.types.InlineKeyboardButton('2', callback_data='2'),
             telebot.types.InlineKeyboardButton('3', callback_data='3'),
             telebot.types.InlineKeyboardButton('+', callback_data='+'))

keyboard.row(telebot.types.InlineKeyboardButton('', callback_data='no'),
             telebot.types.InlineKeyboardButton('0', callback_data='0'),
             telebot.types.InlineKeyboardButton(',', callback_data='.'),
             telebot.types.InlineKeyboardButton('=', callback_data='='))


@bot.message_handler(commands=['start', 'calculater'])
def get_message(message):
    global value
    if value == '':
        bot.send_message(message.from_user.id, '0', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_func(querty):
    global value, old_value
    data = querty.data
    if data == 'no':
        pass
    elif data == 'c':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value)-1]
    elif data == '=':
        try:
            value = str(eval(value))
        except:
            value = 'ошибка'
    else:
        value += data

    if (value != old_value and value != '') or ('0' != old_value and value == ''):
        if value == '':
            bot.edit_message_text(chat_id=querty.message.chat.id,
                                  message_id=querty.message.message_id, text='0', reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=querty.message.chat.id,
                                  message_id=querty.message.message_id, text=value, reply_markup=keyboard)

    old_value = value
    if value == 'ошибка':
        value = ''


print(' bot start')
bot.polling(none_stop=False, interval=0)
