import markup as markup
import telebot
import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('stic/hi.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('₽ Монетка')
    item2 = types.KeyboardButton('🎲 Кости')
    item3 = types.KeyboardButton('♊♌ Гороскоп')

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n"
                                      "Я бот {1.first_name}.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

    low_mess = message.text.lower()
    if low_mess == 'как дела?':
        bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text='Хорошо', callback_data='good')
        item2 = types.InlineKeyboardButton(text='Не очень', callback_data='bad')

    else:
        bot.send_message(message.chat.id, 'Я не знаю что ответить ☹')


@bot.message_handler(content_types=['text'])
def button(message):
    if message.text == '🎲 Кости':
        dice = '⚀⚁⚂⚃⚄⚅'
        bot.send_message(message.chat.id, random.choice(dice))
        bot.send_message(message.chat.id, random.choice(dice))
    elif message.text == '₽ Монетка':
        bot.send_message(message.chat.id, '🪙')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и хорошо☺')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает☹')

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)
