from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler


bot = Bot(token='5717925844:AAE1IjA_6FmDoiy0deyrJVoqRRZzNY3ueGo')
updater = Updater(token='5717925844:AAE1IjA_6FmDoiy0deyrJVoqRRZzNY3ueGo')
dispatcher = updater.dispatcher

START = 0
NUMBERFIRST = 1
NUMBERSECOND = 2
OPERATION = 3
RESULT = 4
numberone = ''
numberTwo = ''
oper = ''


def numbers(number):
    try:
        return int(number)
    except:
        return complex(number.replace(' ', ''))


def result(x, y, z):
    if z == '0':
        return x + y
    elif z == '1':
        return x - y
    elif z == '2':
        return x * y
    return x / y


def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Добро пожаловать в бота, который умеет '
                                                       'считать комплексные и рациональные числа! Напиши 2 числа\n'
                                                       'Введи первое число: ')

    return NUMBERFIRST


def numberFirst(update, context):
    global numberone
    numberone = numbers(update.message.text)
    context.bot.send_message(update.effective_chat.id, 'Отлично!\nВведи второе число: ')

    return NUMBERSECOND


def numberSecond(update, context):
    global numberTwo
    numberTwo = numbers(update.message.text)
    board = [[InlineKeyboardButton('+', callback_data='0'), InlineKeyboardButton('-', callback_data='1')],
             [InlineKeyboardButton('*', callback_data='2'), InlineKeyboardButton(':', callback_data='3')]]
    update.message.reply_text('Выбери:', reply_markup=InlineKeyboardMarkup(board))

    return OPERATION


def operation(update, context):
    global res
    # global oper
    que = update.callback_query
    var = que.data
    que.answer()
    res = result(numberone, numberTwo, var)
    que.edit_message_text(text=f'Результат: {res}')


def cancel(update, context):
    context.bot.send_message(update.effective_chat.id, 'Прощай!')

    return ConversationHandler.END


start_handler = CommandHandler('start', start)
cancel_handler = CommandHandler('cancel', cancel)
numone_handler = MessageHandler(Filters.text, numberFirst)
numtwo_handler = MessageHandler(Filters.text, numberSecond)
oper_handler = CallbackQueryHandler(operation)
conv_handler = ConversationHandler(entry_points=[start_handler],
                                   states={
                                       NUMBERFIRST: [numone_handler],
                                       NUMBERSECOND: [numtwo_handler],
                                       OPERATION: [oper_handler],
                                   },
                                   fallbacks=[cancel_handler])

dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()