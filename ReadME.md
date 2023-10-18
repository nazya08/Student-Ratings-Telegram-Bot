# Student Ratings Telegram Bot

![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)

This Telegram bot is designed to help you track and manage student ratings in your group chats. With this bot, you can easily keep tabs on the performance and contributions of chat members.

## Features

- Track student ratings in real-time.
- View user positions based on their ratings.
- Get general statistics for users in the chat.
- Retrieve monthly statistics for different time periods.

## Usage

To start using the bot, follow these simple instructions:

1. **Adding the Bot to Your Chat:**

    To get started, add the bot to your group chat as an administrator.

2. **Commands:**

    - `/bot_info`: Provides general information about the bot.
    
    - `/my_position`: Shows your current position in the chat based on ratings.
    
    - `/statistics`: Displays general statistics about users in the chat.
    
    - `/statistics_for MM-YYYY`: Shows statistics for the specified month and year in the chat.

3. **Rating Keywords:**

    The bot reacts to specific keywords and symbols in user messages. If a user sends one of these keywords, their rating increases. The keywords include:
    
    - Ukrainian: "дякую", "Дякую", "ДЯКУЮ"
    - Russian: "спасибо", "Спасибо", "СПАСИБО"
    - English: "thanks", "tnx", "thank you", "Thanks", "Tnx", "Thank you", "THANKS", "TNX", "THANK YOU"

4. **Database:**

    The bot uses an SQLite database to store user information, including their name, surname, chat ID, and rating. There are two tables in the database:

    - `users_ratings`: Stores user information, including their name, surname, chat ID, and rating.
    
    - `monthly_rating`: Stores monthly user ratings based on their ID and year.

## Installation

To run the bot successfully, follow these steps:

1. Install the necessary Python libraries:
   - `python-telegram-bot`
   - `python-dotenv`
   - `httpx`

2. Configure the `.env` file with your environment variables, especially `Bot_token`.

3. Ensure the SQLite database, named "tg_bot_rating.db," is in the same directory as your code.

4. Start the bot by calling the `run()` function in your code.

## Important

- Configure the bot according to your needs and ensure it has access to the relevant chats.
- Follow security and confidentiality guidelines when using the bot.

## Project Structure

This project consists of two main files:

1. `main.py`: Contains the code for the Telegram bot and user message handling.

2. `database.py`: Contains the code for managing the SQLite database, including table creation and updating user ratings.

Please make the necessary configurations and ensure proper database access for the bot to work correctly.

## Author

This project was developed by [Nazar Filoniuk](https://github.com/nazya08).
