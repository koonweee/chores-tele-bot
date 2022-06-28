import datetime
from telegram.ext import Updater, CommandHandler
from sheets import *
import pytz
from pytz import timezone
import logging

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
        return (
            '🗑️ Trash: %s\n'
            '🚽 Upstairs toilet: %s\n'
            '🚽 Downstairs toilet: %s\n'
            '🚽 Common toilet: %s\n'
            '🧹 Common floor: %s'
        ) % (chores[0], chores[1], chores[2], chores[3], chores[4])

# chores handler
def chores(update, context):
    today = datetime.datetime.now(tz=pytz.utc)
    today = today.astimezone(timezone('US/Pacific'))
    todayString = today.strftime("%B %d, %Y")
    message = 'Retrieving chores for week of %s...' % todayString
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    message = chores_message(today)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def last_week_chores(update, context):
    today = datetime.datetime.now(tz=pytz.utc)
    today = today.astimezone(timezone('US/Pacific'))
    todayString = today.strftime("%B %d, %Y")
    message = 'Retrieving chores for week of %s...' % todayString
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    message = chores_message(today  + datetime.timedelta(-7))
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def next_week_chores(update, context):
    today = datetime.datetime.now(tz=pytz.utc)
    today = today.astimezone(timezone('US/Pacific'))
    todayString = today.strftime("%B %d, %Y")
    message = 'Retrieving chores for week of %s...' % todayString
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    message = chores_message(today  + datetime.timedelta(7))
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def chores_done(update, context):


chores_handler = CommandHandler('chores', chores) # associate /start with above fn
last_week_chores_handler = CommandHandler('last_week_chores', last_week_chores) # associate /start with above fn
next_week_chores_handler = CommandHandler('next_week_chores', next_week_chores) # associate /start with above fn
dispatcher.add_handler(chores_handler)
dispatcher.add_handler(last_week_chores_handler)
dispatcher.add_handler(next_week_chores_handler)
updater.start_polling()
