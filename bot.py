import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU')

date = datetime.now()

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY={'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def where_is_a_planet(planet):
    try:
        ephem_planet = getattr(ephem, planet.capitalize())(date)
        cons = f'Планета {planet.capitalize()} сегодня находится в созвездии {ephem.constellation(ephem_planet)[1]}.'
        return cons
    except (AttributeError, KeyError):
        return(f'Мне ничего не известно о планете {planet.capitalize()}.')



def find_a_planet(update, context):
    planet = update.message.text.split()[1].lower()
    cons = where_is_a_planet(planet)
    update.message.reply_text(cons)

def greet_user(update, context):
#    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду \\start')

def talk_to_me(update, context):
    user_text = update.message.text

    update.message.reply_text(user_text)

def get_user_message(input_text, len_command):
    output_text = input_text[len_command:].strip()
    return output_text

def word_count(update, context):
    phrase = get_user_message(update.message.text, 10)
    answer = f'Фраза \'{phrase}\' состоит из {len(phrase.split())} слов.' if len(phrase) > 0 else 'Сообщение не должно быть пустым!'
    update.message.reply_text(answer)

def next_full_moon(update, context):
    text_message = get_user_message(update.message.text, 15)
    user_date = datetime.strptime(text_message, '%Y/%m/%d')
    full_moon_date = str(ephem.next_full_moon(user_date))
    next_full_moon = ephem.next_full_moon(user_date)
    date_next_full_moon = datetime.strptime(str(next_full_moon), '%Y/%m/%d %H:%M:%S')
    if date_next_full_moon > datetime.now():
        update.message.reply_text(f'Ближайшее полнолуние после {user_date.strftime("%d.%m.%Y")} будет {date_next_full_moon.strftime("%d.%m.%Y")}.')
    else:
        update.message.reply_text(f'Ближайшее полнолуние после {user_date.strftime("%d.%m.%Y")} было {date_next_full_moon.strftime("%d.%m.%Y")}.')

def main():
    
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", find_a_planet))
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()