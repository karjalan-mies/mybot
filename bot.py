from emoji import emojize
from glob import glob
import logging
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
from datetime import datetime
import locale
import os.path
locale.setlocale(locale.LC_TIME, 'ru_RU')


logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY={'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}
dict_users = {}
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


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f'Привет, пользователь {context.user_data["emoji"]}!')


def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    user_text = update.message.text
    update.message.reply_text(f'{user_text} {context.user_data["emoji"]}')


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


def test_cities(update, context):
    users_message_text = get_user_message(update.message.text, 5)
    user_name = str(update.message.chat.first_name)
    context.user_data[user_name].append(users_message_text)

    return users_message_text[-1::-1]


def test_def(update, context):
    user_name = update.message.chat.first_name
    user_message = get_user_message(update.message.text, 5)
    user_list = {}
    if os.path.isfile('users.csv'):
        update.message.reply_text(f'Файл существует')
    else:
        user_list['name'] = user_name
        user_list['cities'] = user_message.encode()
        update.message.reply_text(f'cities содержит {user_message}')
        update.message.reply_text(user_list)
        with open('users.csv', 'w') as f:
            fields = ['name', 'cities', 'first_letter']
            writer = csv.DictWriter(f, fields, delimiter = ';')
            writer.writeheader()
            for user in user_list:
                writer.writerow(user)


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое число {bot_number}. Вы выиграли!"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, мое число {bot_number}. Ничья!"
    else:
        message = f"Ваше число {user_number}, мое число {bot_number}. Вы проиграли!"
    return message


def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)


def send_cat_picture(update, context):
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'))


def main():    
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", find_a_planet))
    dp.add_handler(CommandHandler("word_count", word_count))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(CommandHandler("test", test_def))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()
