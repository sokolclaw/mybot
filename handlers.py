import logging
import ephem
import datetime

from utiles import action_bot_city, action_user_city, precalculate, show_keyboard
from telegram.ext import ConversationHandler

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start',
                              reply_markup = show_keyboard()
                              )
    

def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def where_planet(update, context):
    user_text = context.args
    planets = {'марс':  ephem.Mars, 'меркурий':  ephem.Mercury, 'венера':  ephem.Venus, 'юпитер':  ephem.Jupiter,
               'нептун':  ephem.Neptune, 'сатурн':  ephem.Saturn, 'уран':  ephem.Uranus, 'плутон':  ephem.Pluto 
            }
    planet = planets[user_text[0].lower()](datetime.date.today()) 
    constellation = ephem.constellation(planet)
    print(constellation)
    update.message.reply_text(constellation, reply_markup = show_keyboard())    


def how_many_words(update, context):
    user_text = context.args
    if not len(user_text):
        update.message.reply_text('В этом сообщении нет слов')
    else:
        update.message.reply_text(len(user_text), reply_markup = show_keyboard())
    print(len(user_text))


def when_fool_moon(update, context):
    user_text = context.args
    data = user_text[0].split('.')
    moon = ephem.next_full_moon(f'{data[2]}-{data[1]}-{data[0]}')
    update.message.reply_text(moon)


def calculate(update, context):
    user_text = ''.join(context.args)
    a = user_text.replace(' ', '')
    parts = a.split('+')
    for plus in range(len(parts)):
        if '-' in parts[plus]:
            parts[plus] = parts[plus].split('-')
    for plus in range(len(parts)):
        parts[plus] = precalculate(parts[plus])
    update.message.reply_text(sum(parts), reply_markup = show_keyboard())


def start_playing(update, context):
    update.message.reply_text('Начинаем игру в города.  Называй первый город\n'
                              'Чтобы остановить игру введи /stop')
    return 'answer'


def playing_in_cities(update, context):
    with open('cities.txt', 'r') as cities:
        cities_list = cities.read().lower().split(', ')
    if 'cities' not in context.user_data:
        context.user_data['cities'] = ['.',]
    if 'alpha' not in context.user_data:
        context.user_data['alpha'] = ''
    if not cities_list[-1]:
        cities_list = cities_list[:-1]
    if not cities_list:
        return 'Города закончились :('
    action_user_city(update, context, cities_list)
    action_bot_city(update, context, cities_list)


def stop_playing(update, context):
    user_text = update.message.text
    logging.info('Остановка игры')
    update.message.reply_text('Останавливаем игру')
    return ConversationHandler.END


def user_coordinates(update, context):
    coords = update.message.location
    update.message.reply_text(
        f'Ваши координаты: {coords}',
        reply_markup = show_keyboard()
        )