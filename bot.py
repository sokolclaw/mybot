import logging
import settings

from handlers import (greet_user, where_planet, how_many_words, when_fool_moon, calculate,
                      user_coordinates, talk_to_me, start_playing, stop_playing, playing_in_cities)
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters


logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    cities_handler = ConversationHandler(
        entry_points=[
            CommandHandler('cities', start_playing),
            MessageHandler(Filters.regex('(Сыграем в города?)'), start_playing)
            ],
        states={
            'answer': [MessageHandler(Filters.text & ~Filters.command & ~Filters.regex('(Остановить игру)'), playing_in_cities)]
            },
        fallbacks=[
            CommandHandler('stop', stop_playing),
            MessageHandler(Filters.regex('(Остановить игру)'), stop_playing)]
        ,)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', where_planet))
    dp.add_handler(CommandHandler('wordcount', how_many_words))
    dp.add_handler(CommandHandler('next_fool_moon', when_fool_moon))
    dp.add_handler(cities_handler)
    dp.add_handler(CommandHandler('calc', calculate))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
 

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()
    
    
if __name__ == '__main__':
    main()
