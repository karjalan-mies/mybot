from datetime import datetime
import ephem
from glob import glob
from random import choice

from utils import where_is_a_planet, get_smile, get_user_message, play_random_numbers, main_keyboard

def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f'Привет, пользователь {context.user_data["emoji"]}!',
        reply_markup=main_keyboard()
    )


def find_a_planet(update, context):
    planet = update.message.text.split()[1].lower()
    cons = where_is_a_planet(planet)
    update.message.reply_text(cons)


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
    update.message.reply_text(message,
                              reply_markup=main_keyboard()
                              )


def send_cat_picture(update, context):
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'),
                           reply_markup=main_keyboard()
                           )


def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f'Ваши координаты {coords} {context.user_data["emoji"]}!',
        reply_markup=main_keyboard()
    )


def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    user_text = update.message.text
    update.message.reply_text(f'{user_text} {context.user_data["emoji"]}',
                              reply_markup=main_keyboard()
                              )
