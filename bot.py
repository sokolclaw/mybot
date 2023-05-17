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
    user_text = update.message.text.split()
    planets = {'марс':  ephem.Mars, 'меркурий':  ephem.Mercury, 'венера':  ephem.Venus, 'юпитер':  ephem.Jupiter,
               'нептун':  ephem.Neptune, 'сатурн':  ephem.Saturn, 'уран':  ephem.Uranus, 'плутон':  ephem.Pluto 
            }
    planet = planets[user_text[1].lower()](datetime.date.today()) 
    constellation = ephem.constellation(planet)
    print(constellation)
    update.message.reply_text(constellation)
    
def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', where_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()
    
    
if __name__ == '__main__':
    main()
