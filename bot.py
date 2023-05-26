import logging
import settings
import ephem
import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


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
    if len(user_text) == 0:
        update.message.reply_text('В этом сообщении нет слов')
    else:
        update.message.reply_text(len(user_text))
    print(len(user_text))
    
def when_fool_moon(update, context):
    user_text = context.args
    data = user_text[0].split('.')
    moon = ephem.next_full_moon(f'{data[2]}-{data[1]}-{data[0]}')
    update.message.reply_text(moon)
    
def playing_in_cities(update, context):
    with open('cities.txt', 'r') as cities:
        cities_list = cities.read().lower().split(', ')
    user_text = ' '.join(context.args).lower()

    if user_text not in cities_list:
        update.message.reply_text('Слово не подходит')
    cities_list.remove(user_text)
    alpha = user_text[-1] if user_text[-1] != 'ь' else user_text[-2]
    if not cities_list:
        return
    if not cities_list[-1]:
        cities_list = cities_list[:-1]
    answers_can_be = [city for city in cities_list if city[0] == alpha]
    update.message.reply_text(answers_can_be[0].title())
    answers_can_be.clear()



def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', where_planet))
    dp.add_handler(CommandHandler('wordcount', how_many_words))
    dp.add_handler(CommandHandler('next_fool_moon', when_fool_moon))
    dp.add_handler(CommandHandler('cities', playing_in_cities))
    dp.add_handler(CommandHandler('calc', calculate))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()
    
    
if __name__ == '__main__':
    main()
