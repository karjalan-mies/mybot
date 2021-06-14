import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import locale

from hendlers import (greet_user, find_a_planet, word_count, next_full_moon, guess_number, send_cat_picture,
                      user_coordinates, talk_to_me)

locale.setlocale(locale.LC_TIME, 'ru_RU')
logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY={'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
                                                                 'password': settings.PROXY_PASSWORD}}
dict_users = {}

def main():    
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", find_a_planet))
    dp.add_handler(CommandHandler("word_count", word_count))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()
