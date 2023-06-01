import logging
import settings
import ephem
import datetime
from random import choice

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters


logging.basicConfig(filename='bot.log', level=logging.INFO)
        
def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

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
    update.message.reply_text(constellation)

def how_many_words(update, context):
    user_text = context.args
    if not len(user_text):
        update.message.reply_text('В этом сообщении нет слов')
    else:
        update.message.reply_text(len(user_text))
    print(len(user_text))
    
def when_fool_moon(update, context):
    user_text = context.args
    data = user_text[0].split('.')
    moon = ephem.next_full_moon(f'{data[2]}-{data[1]}-{data[0]}')
    update.message.reply_text(moon)

def action_user_city(update, context, cities):
    user_text = update.message.text.lower()
    if user_text not in cities:
        update.message.reply_text('Такого слова нет в списке')
        return 'error'
    cities.remove(user_text)
    if len(context.user_data['cities']) > 2:
        if context.user_data['alpha'] != user_text[0]:
            update.message.reply_text(f"Назови город на букву {context.user_data['alpha']}")
            return 'error'
    if user_text in context.user_data['cities']:
        update.message.reply_text('Этот город уже был')
        return 'error'
    context.user_data['alpha'] = user_text[-1] if user_text[-1] not in ['ь', 'ы'] else user_text[-2]
    context.user_data['cities'].append(user_text)
    return user_text

def action_bot_city(update, context, cities):
    answers_can_be = [city for city in cities
                     if city[0] == context.user_data['alpha'] and city not in context.user_data['cities']]  
    bot_city = choice(answers_can_be)
    cities.remove(bot_city)
    update.message.reply_text(bot_city.title())
    context.user_data['cities'].append(bot_city)
    answers_can_be.clear()
    context.user_data['alpha'] = bot_city[-1] if bot_city[-1] not in ['ь', 'ы'] else bot_city[-2]

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
    user_answer = action_user_city(update, context, cities_list)
    if user_answer != 'error':
        action_bot_city(update, context, cities_list)

def calculate(update, context):
    user_text = ''.join(context.args)
    a = user_text.replace(' ', '')
    parts = a.split('+')
    for plus in range(len(parts)):
        if '-' in parts[plus]:
            parts[plus] = parts[plus].split('-')
    for plus in range(len(parts)):
        parts[plus] = precalculate(parts[plus])
    update.message.reply_text(sum(parts))

def precalculate(part):
    if type(part) is str:
        if '*' in part:
            result = 1
            for subpart in part.split('*'):
                result *= precalculate(subpart)
            return result
        elif '/' in part:
            parts = list(map(precalculate, part.split('/')))
            result = parts[0]
            for subpart in parts[1:]:
                result /= subpart
            return result
        else:
            return float(part)
    elif type(part) is list:
    
        for i in range(len(part)):
            part[i] = precalculate(part[i])
        return part[0]-sum(part[1:])
    return part

def start_playing(update, context):
    update.message.reply_text('Начинаем игру в города.  Называй первый город\n'
                              'Чтобы остановить игру введи /stop')
    return 'answer'

def stop_playing(update, context):
    user_text = update.message.text
    logging.info('Остановка игры')
    update.message.reply_text('Останавливаем игру')
    return ConversationHandler.END

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    cities_handler = ConversationHandler(
        entry_points=[CommandHandler('cities', start_playing)],
        states={'answer': [MessageHandler(Filters.text & ~Filters.command, playing_in_cities)]},
        fallbacks=[CommandHandler('stop', stop_playing)],)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', where_planet))
    dp.add_handler(CommandHandler('wordcount', how_many_words))
    dp.add_handler(CommandHandler('next_fool_moon', when_fool_moon))
    dp.add_handler(cities_handler)
    dp.add_handler(CommandHandler('calc', calculate))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
 

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()
    
    
if __name__ == '__main__':
    main()
