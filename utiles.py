
from random import choice
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton



def show_keyboard():
    return ReplyKeyboardMarkup([['Сыграем в города?', KeyboardButton('Мои координаты', request_location=True)]])
    

def action_user_city(update, context, cities):
    user_text = update.message.text.lower()
    if user_text not in cities:
        update.message.reply_text('Такого слова нет в списке')
        raise ValueError
    cities.remove(user_text)
    if len(context.user_data['cities']) > 2:
        if context.user_data['alpha'] != user_text[0]:
            update.message.reply_text(
                f"Назови город на букву {context.user_data['alpha']}", reply_markup = show_keyboard())
            raise ValueError
    if user_text in context.user_data['cities']:
        update.message.reply_text('Этот город уже был', reply_markup = show_keyboard())
        raise ValueError
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

