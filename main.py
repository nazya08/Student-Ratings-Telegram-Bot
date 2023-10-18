import os
import logging

from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder, \
    filters, MessageHandler

from dotenv import load_dotenv
from database import *

load_dotenv()
API_KEY = os.getenv('Bot_token')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARNING)

# Ключові слова
ukr_words = ["дякую", "Дякую", "ДЯКУЮ"]
rus_words = ["спасибо", "Спасибо", "СПАСИБО"]
eng_words = ["thanks", "tnx", "thank you", "Thanks", "Tnx", "Thank you", "THANKS", "TNX", "THANK YOU"]
key_symbols = ["👍", "+", ukr_words, rus_words, eng_words]


async def bot_info(update: Update, context: CallbackContext) -> None:
    logging.info("Function 'bot_info' built succesfully")

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"""Hi there, i'm your bot assistant for tracking"""
                                        """the rating of students in group chats. :)\n\n"""
                                        """Bot commands:\n- /bot_info (general info about bot)"""
                                        """\n- /my_position (your position in current chat by rating)"""
                                        """\n- /statistics (general statistics for users in this chat)"""
                                        """\n- /statistics_for {month}-{year} (statistics for current month and year)""")


async def process_message(update: Update, context: CallbackContext) -> None:
    logging.info("Function 'process_message' built successfully")

    user = update.message.from_user

    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    chat_id = update.message.chat_id
    current_date = datetime.now()
    month = current_date.month
    year = current_date.year

    try:
        if update.message and update.message.text:
            text = update.message.text

            # Перевірка, чи користувач відповідає на повідомлення бота
            if update.message.reply_to_message is None:
                # Якщо користувач надсилає просте повідомлення, перевіряємо наявність слів з key_symbols
                if any(text in symbol for symbol in key_symbols):
                    # Якщо користувач надсилає повідомлення, яке є в key_symbols,
                    # додати бал до рейтингу користувача

                    fill_users_ratings_table(user_id, first_name, last_name, chat_id, month, year)
            else:
                # Якщо користувач відповідає на повідомлення бота, можна додати відповідь
                text = text.lower()  # Перетворюємо текст на нижній регістр для перевірки
                if any(word in text for word in ukr_words):
                    await update.message.reply_text('Завжди радий допомогти!')
                elif any(word in text for word in rus_words):
                    await update.message.reply_text('Всегда рад помочь!')
                elif any(word in text for word in eng_words):
                    await update.message.reply_text('It is my pleasure!')
    except Exception as e:
        # Обробка будь-яких інших помилок
        logging.error(f"Error while processing message: {str(e)}")


async def my_position(update: Update, context: CallbackContext) -> None:
    logging.info("Function 'my_position' built successfully")

    user = update.message.from_user

    user_id = user.id
    chat_id = update.message.chat_id
    chat_title = update.message.chat.title

    await update.message.reply_text(f'Your current position in << {chat_title} >> :  {get_user_position(user_id, chat_id)}')


async def statistics(update: Update, context: CallbackContext) -> None:
    logging.info("Function 'statistics' built successfully")

    chat_id = update.message.chat_id

    get_statistics_db = get_statistics(chat_id)

    if get_statistics_db:
        await update.message.reply_text(get_statistics_db)
    else:
        await update.message.reply_text("No statistics available for this chat.")


async def monthly_statistics(update: Update, context: CallbackContext) -> None:
    logging.info("Function 'monthly_statistics' built successfully")

    chat_id = update.message.chat_id
    chat_title = update.message.chat.title

    # Розділення аргументів місяця та року з команди
    command_parts = context.args[0].split('-')
    if len(command_parts) != 2:
        await update.message.reply_text("Invalid command format. Please use '/statistics MM-YYYY' format.")
        return

    try:
        month = int(command_parts[0])
        year = int(command_parts[1])
    except ValueError:
        await update.message.reply_text("Invalid month or year format. Please use '/statistics MM-YYYY' format.")
        return

    get_monthly_statistics_db = get_monthly_statistics(chat_id, month, year, chat_title)

    if get_monthly_statistics_db:
        await update.message.reply_text(get_monthly_statistics_db)
    else:
        await update.message.reply_text("No statistics available for this period.")


def run():
    logging.info("Application built succesfully")

    app = ApplicationBuilder().token(API_KEY).read_timeout(30).write_timeout(30).build()
    app.add_handler(CommandHandler("bot_info", bot_info))
    app.add_handler(MessageHandler(filters.ALL & ~filters.Command(), process_message))
    app.add_handler(CommandHandler("my_position", my_position))
    app.add_handler(CommandHandler("statistics", statistics))
    app.add_handler(CommandHandler("statistics_for", monthly_statistics))

    app.run_polling(poll_interval=7)

    database_bot()


if __name__ == '__main__':
    run()

