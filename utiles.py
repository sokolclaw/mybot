
from random import choice
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


def show_keyboard(status):
    if status == 'base':
        return ReplyKeyboardMarkup(
            [['Сыграем в города?', KeyboardButton('Мои координаты', request_location=True)]]
                                   )
    if status == 'cities':
        return ReplyKeyboardMarkup([['Остановить игру']])

def action_with_city(update, context, city):

    context.user_data['start_cities'].remove(city)
    context.user_data['alpha'] = city[-1] if city[-1] not in ['ь', 'ы'] else city[-2]
    context.user_data['cities'].append(city)


def action_user_city(update, context):

    user_text = update.message.text.lower()
    if user_text not in context.user_data['start_cities'] and user_text not in context.user_data['cities']:
        return update.message.reply_text('Я такого города не знаю')
    if len(context.user_data['cities']) > 1:
        if context.user_data['alpha'] != user_text[0]:
            return update.message.reply_text(
                f"Назови город на букву {context.user_data['alpha']}")
    if user_text in context.user_data['cities']:
        return update.message.reply_text('Этот город уже был', reply_markup = show_keyboard('cities'))
    
    action_with_city(update, context, user_text)
    action_bot_city(update, context)

def action_bot_city(update, context):

    answers_can_be = [city for city in context.user_data['start_cities']
                     if city[0] == context.user_data['alpha'] and city not in context.user_data['cities']]  
    bot_city = choice(answers_can_be)
    update.message.reply_text(bot_city.title(), reply_markup = show_keyboard('cities'))
    action_with_city(update, context, bot_city)
    answers_can_be.clear()


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

