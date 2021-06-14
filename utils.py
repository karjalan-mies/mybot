from emoji import emojize
import ephem
from random import choice, randint
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

def where_is_a_planet(planet):
    try:
        ephem_planet = getattr(ephem, planet.capitalize())(date)
        cons = f'Планета {planet.capitalize()} сегодня находится в созвездии {ephem.constellation(ephem_planet)[1]}.'
        return cons
    except (AttributeError, KeyError):
        return(f'Мне ничего не известно о планете {planet.capitalize()}.')


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def get_user_message(input_text, len_command):
    output_text = input_text[len_command:].strip()
    return output_text


def test_cities(update, context):
    users_message_text = get_user_message(update.message.text, 5)
    user_name = str(update.message.chat.first_name)
    context.user_data[user_name].append(users_message_text)

    return users_message_text[-1::-1]


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое число {bot_number}. Вы выиграли!"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, мое число {bot_number}. Ничья!"
    else:
        message = f"Ваше число {user_number}, мое число {bot_number}. Вы проиграли!"
    return message


def main_keyboard():
    return ReplyKeyboardMarkup([['Прислать котика', KeyboardButton('Мои координаты', request_location=True)]])