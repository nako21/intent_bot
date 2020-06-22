# pip install python_telegram_bot

# Код бота

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = 'TOKEN'

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)

def text(update, context):
    """Ответ уже от движка"""
    answer = Updater.generate_answer(update.message.text)
    print(update.message.text, '->', answer)
    print(update.stats)
    print()
    update.message.reply_text(answer)

def error(update, context):
    update.message.reply_text('Я работаю только с текстом')

def main():
    # pip install pysocks
    REQUEST_KWARGS= {'proxy_url': 'socks5'}
    updater = Updater(TOKEN, request_kwargs={'proxy_url': 'socks5://109.194.175.135:9050'}, use_context=True)
    
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
#   dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, text))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
    main()


