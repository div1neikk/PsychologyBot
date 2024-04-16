import os
from dotenv import load_dotenv

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

import google.generativeai as genai

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TG_TOKEN")
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет! Я бот, который поможет тебе решить социальные проблемы. Расскажи мне, что тебя беспокоит.")


def get_gemini_response(prompt):
    model = genai.GenerativeModel('models/gemini-pro')
    result = model.generate_content(prompt)
    return result.text


def handle_message(update, context):
    user_message = update.message.text
    loading_message = context.bot.send_message(chat_id=update.effective_chat.id, text="Ваш запрос обрабатывается...")
    loading_message_id = loading_message.message_id
    gemini_response = get_gemini_response(user_message).replace('*', '')
    context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=loading_message_id, text=gemini_response)


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
