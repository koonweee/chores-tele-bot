import datetime
from distutils.log import error
from telegram.ext import Updater, CommandHandler
from sheets import *
import pytz
from pytz import timezone
import logging

chores_map = {
    'trash': 1,
    'upstairs_toilet': 2,
    'downstairs_toilet': 3,
    'common_toilet': 4,
    'common_floor': 5
}

updater = Updater(token='5138358228:AAF50OgNglW72Y69TFmeRTHGqQ9n1HVdsVo',
    use_context=True) # receives updates from Telegram
dispatcher = updater.dispatcher # dispatches updates to appropriate handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO) # config for logger

def chores_message(date):
    chores = getWeekChores(date)
    if not chores:
        return 'Chores not found.'
    else:
        return ((
            '🗑️ Trash: %s\n' 
            '🚽 Upstairs toilet: %s\n'
            '🚽 Downstairs toilet: %s\n'
            '🚽 Common toilet: %s\n'
            '🧹 Common floor: %s'
        ) % (chores[0], chores[1], chores[2], chores[3], chores[4])).replace('DONE', 'DONE ✅')

def chores_help(update,context):
    help_message = '/help - help\n/chores <OPTIONAL: prev/next> - list of chores for current week, specify prev or next for other weeks\n/chores_done <trash/upstairs_toilet/downstairs_toilet/common_toilet/common_floor> - set specified chore for current week as done'
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)


# chores handler
def chores(update, context):
    today = datetime.datetime.now(tz=pytz.utc)
    today = today.astimezone(timezone('US/Pacific'))
    if len(context.args) > 0:
        arg = context.args[0]
        if arg == 'prev':
            today += datetime.timedelta(-7)
        if arg == 'next':
            today += datetime.timedelta(7)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Invalid option, please specify prev, next or no options')
            return

    todayString = today.strftime("%B %d, %Y")
    message = 'Retrieving chores for week of %s...' % todayString
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    message = chores_message(today)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def chores_done(update, context):
    error_message = 'Please follow the format: /chores_done <trash/common_floor/upstairs_toilet/lower_toilet/common_toilet>'
    if len(context.args) > 0:
        what = context.args[0]
        if what in chores_map:
            today = datetime.datetime.now(tz=pytz.utc)
            today = today.astimezone(timezone('US/Pacific'))
            updateDoneChore(today, chores_map[what])
            message = '{} marked as done'.format(what)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)

chores_handler = CommandHandler('chores', chores) # associate /start with above fn
chores_done_handler = CommandHandler('chores_done', chores_done) # associate /start with above fn
chores_help_handler = CommandHandler('chores_help', chores_help) # associate /start with above fn
dispatcher.add_handler(chores_handler)
dispatcher.add_handler(chores_done_handler)
dispatcher.add_handler(chores_help_handler)
updater.start_polling()

