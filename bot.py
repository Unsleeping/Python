import pyowm
import telebot
import config
import random

from telebot import types

from config import lv_messages as list_of_love_messages
from config import ht_messages as list_of_hate_messages
from config import ht_stickers as list_of_hate_stickers
from config import lv_stickers as list_of_love_stickers
from config import haters as list_of_haters

bot = telebot.TeleBot(config.token)
owm = pyowm.OWM(config.owm_token)


@bot.message_handler(commands=['start', 'Start'])
def start_message(message):
    keyboard2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_language = types.KeyboardButton(text="/language")
    button_geolocation = types.KeyboardButton(text="/geolocation")
    keyboard2.add(button_language, button_geolocation)
    bot.send_message(message.chat.id,
                     "Hello {0.first_name}!\nI am - <b>{1.first_name}</b>.".format(message.from_user,
                                                                                   bot.get_me()), parse_mode='html',
                     reply_markup=keyboard2)
    bot.send_message(message.chat.id,
                     "Please tell me the place where you want to know the weather or send me your location.")


def check_city_in_the_message(string, cities):
    words = string.lower().split(" ")
    flag = False
    for check_city in words:
        if cities[:-1].lower() == check_city[:-1] and not flag:
            flag = True
    return flag


def send_smth_to_lovers_and_haters():
    bot.send_sticker(config.Xenia, random.choice(list_of_love_stickers))
    bot.send_message(config.Xenia, random.choice(list_of_love_messages))
    bot.send_message(random.choice(list_of_haters), random.choice(list_of_hate_messages))
    bot.send_sticker(random.choice(list_of_haters), random.choice(list_of_hate_stickers))


def answer_depends_on_the_temp(temp, answer):
    if temp < 10:
        answer += 'There is cold enough, please buy some coffee on your way'

    elif temp < 0:
        answer += 'There is very cold, just sit at home and drink hot tea with some pancakes'

    elif temp < 20:
        answer += 'There is not bad to go outside'

    else:
        answer += 'There is a good weather to go outside'

    return answer


@bot.message_handler(commands=['language'])
def select_language(message):
    keyboard2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_lang_ru = types.KeyboardButton(text="ru")
    button_lang_eng = types.KeyboardButton(text="eng")
    keyboard2.add(button_lang_ru, button_lang_eng)
    bot.send_message(message.chat.id, 'There are some problems, try that next time')
    bot.send_sticker(message.chat.id, config.stk_list[1])


# # @bot.message_handler(commands=['ru'])
# # def setup_ru():
# #     language = 'ru'
# #     owm = pyowm.OWM('ea82df064d9a6a63e8323033072b9c15', language)
# #     return owm
# #
# #
# # @bot.message_handler(commands=['eng'])
# # def setup_eng():
# #     owm = pyowm.OWM('ea82df064d9a6a63e8323033072b9c15')
# #


@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    print(message)
    if message.chat.id == config.Xenia:
        bot.send_message(message.chat.id, 'U R so beautiful')
        bot.send_sticker(message.chat.id, random.choice(list_of_love_stickers))

    elif list_of_haters.count(message.chat.id) == 1:
        bot.send_sticker(config.Alim, random.choice(list_of_hate_stickers))

    else:
        send_smth_to_lovers_and_haters()


@bot.message_handler(commands=["geolocation"])
def geolocation(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Send location", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Send me your location and I will guess the weather there", reply_markup=keyboard)


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard1.row('/start')
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        observation = owm.weather_around_coords(message.location.latitude, message.location.longitude, limit=8)
        w = observation[0].get_weather()
        print(w)
        temp = w.get_temperature('celsius')["temp"]
        answer = 'The weather in your location: ' + w.get_detailed_status() + "\n"
        answer += 'Temperature now is ' + str(temp) + "\n\n"
        answer = answer_depends_on_the_temp(temp, answer)
        bot.send_message(message.chat.id, answer, reply_markup=keyboard1)
        print('bot said: ' + str(answer))


@bot.message_handler(content_types=['text'])
def send_echo(message):
    print(message.from_user.first_name + " said: " + message.text)
    if config.thx_list.count(message.text.lower()) >= 1:
        bot.send_sticker(message.chat.id, config.stk_list[2])

    elif config.hwy_list.count(message.text.lower()) >= 1:

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("I'm OK", callback_data='good')
        item2 = types.InlineKeyboardButton('So so', callback_data='bad')

        markup.add(item1, item2)

        bot.send_message(message.chat.id, 'I am so sad, and you?', reply_markup=markup)
        bot.send_sticker(message.chat.id, config.stk_list[0])

    elif config.hi_list.count(message.text.lower()) >= 1:
        bot.send_sticker(message.chat.id, config.stk_list[3])

    elif config.why_list.count(message.text.lower()) >= 1:
        bot.send_message(message.chat.id, 'because')
        bot.send_sticker(message.chat.id, config.stk_list[4])

    elif config.love_list.count(message.text.lower()) >= 1:
        bot.send_sticker(message.chat.id, config.stk_list[5])

    else:
        try:
            if check_city_in_the_message(str(message.text), 'москва'):
                observation = owm.weather_at_place('Москва')
                message.text = 'Москва'
            else:
                observation = owm.weather_at_place(message.text)
            w = observation.get_weather()
            temp = w.get_temperature('celsius')["temp"]
            answer = 'In the city: ' + message.text + ' ' + w.get_detailed_status() + "\n"
            answer += 'Temperature now is ' + str(temp) + "\n\n"
            answer = answer_depends_on_the_temp(temp, answer)
            bot.send_message(message.chat.id, answer)
            print('bot said: ' + str(answer))
        except:
            keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard1.row('/start')
            bot.send_message(message.chat.id, "If u want to get the basic information, press the button below",
                             reply_markup=keyboard1)
            if message.chat.id == config.Mandr1k:

                while True:
                    bot.send_message(random.choice(list_of_haters), random.choice(list_of_hate_messages))
                    print(random.choice(list_of_hate_messages))
                    bot.send_sticker(random.choice(list_of_haters), random.choice(list_of_hate_stickers))

                send_smth_to_lovers_and_haters()

            elif list_of_haters.count(message.chat.id) == 1:
                # random.seed(random.random())
                bot.send_message(message.chat.id, random.choice(list_of_hate_messages))
                print(random.choice(list_of_hate_messages))
                bot.send_sticker(message.chat.id, random.choice(list_of_hate_stickers))

            else:
                bot.send_message(message.chat.id, "Sorry, I don't understand you")
                bot.send_sticker(message.chat.id, config.stk_list[6])
                bot.send_message(message.chat.id, 'If it was the place, try to send it again')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, "That's great!")
                bot.send_message(call.message.chat.id, 'Maybe you want to know about the weather? Just end me the '
                                                       'place.')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id,
                                 "Oh, maybe the weather forecast will help you? Send me the place")

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='I am so '
                                                                                                         'sad, '
                                                                                                         'and you?',
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='Just send me the place, omg')
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    bot.polling(none_stop=True)