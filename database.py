import sqlite3
from os import path


ROOT = path.dirname(path.realpath(__file__))


def database_bot():
    with sqlite3.connect(path.join(ROOT, "tg_bot_rating.db")) as db:
        cursor = db.cursor()

        # Create users_ratings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                first_name TEXT,
                last_name TEXT,
                chat_id TEXT,
                rating INTEGER
            );
        ''')

        # Create rating_by_months
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_rating (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                month INTEGER,
                year INTEGER,
                rating INTEGER,
                FOREIGN KEY (user_id) REFERENCES users_ratings (id)
            );
        ''')

        db.commit()


def fill_users_ratings_table(user_id, first_name, last_name, chat_id, month, year):
    with sqlite3.connect(path.join(ROOT, "tg_bot_rating.db")) as db:
        cursor = db.cursor()

        cursor.execute(''' SELECT rating 
                        FROM users_ratings 
                        WHERE user_id=? AND chat_id=? ''', (user_id, chat_id))

        user_rating = cursor.fetchone()

        if user_rating:
            cursor.execute(''' UPDATE users_ratings 
                            SET rating=rating+1 
                            WHERE user_id=? AND chat_id=? ''', (user_id, chat_id))
            cursor.execute(''' SELECT id FROM users_ratings 
                            WHERE user_id=? AND chat_id=? ''', (user_id, chat_id))
            user_id_in_ratings = cursor.fetchone()[0]
        else:
            cursor.execute(''' INSERT INTO users_ratings (user_id, first_name, last_name, chat_id, rating) 
                            VALUES (?, ?, ?, ?, 1) ''', (user_id, first_name, last_name, chat_id))
            user_id_in_ratings = cursor.lastrowid

        # Перевірка, чи запис вже існує в monthly_rating
        cursor.execute(''' SELECT id, rating, month
                        FROM monthly_rating
                        WHERE user_id=? AND year=? ''', (user_id_in_ratings, year))

        monthly_record = cursor.fetchone()

        if monthly_record:
            # Якщо запис існує, оновлюємо рейтинг тільки, якщо місяць співпадає з поточним
            if monthly_record[2] == month:
                new_rating = monthly_record[1] + 1
                cursor.execute(''' UPDATE monthly_rating 
                                SET rating=? 
                                WHERE id=? ''', (new_rating, monthly_record[0]))
            else:
                # Якщо місяць не співпадає, додаємо новий рядок
                cursor.execute(''' INSERT INTO monthly_rating (user_id, month, year, rating) 
                                VALUES (?, ?, ?, 1) ''', (user_id_in_ratings, month, year))
        else:
            # Якщо запису немає, то створюємо новий рядок
            cursor.execute(''' INSERT INTO monthly_rating (user_id, month, year, rating) 
                            VALUES (?, ?, ?, 1) ''', (user_id_in_ratings, month, year))

        db.commit()


def get_user_position(user_id, chat_id):
    with sqlite3.connect(path.join(ROOT, "tg_bot_rating.db")) as db:
        cursor = db.cursor()

        cursor.execute(''' SELECT rating 
                        FROM users_ratings 
                        WHERE user_id=? AND chat_id=? ''', (user_id, chat_id))

        user_rating = cursor.fetchone()

        if user_rating:
            user_rating = user_rating[0]

            cursor.execute(''' SELECT COUNT(*) 
                            FROM users_ratings 
                            WHERE rating > ? AND chat_id=? ''', (user_rating, chat_id))

            position = cursor.fetchone()

            if position:
                position = position[0] + 1

                return position


def get_statistics(chat_id):
    with sqlite3.connect(path.join(ROOT, "tg_bot_rating.db")) as db:
        cursor = db.cursor()

        cursor.execute(''' SELECT first_name, last_name, rating 
                        FROM users_ratings 
                        WHERE users_ratings.chat_id=? 
                        ORDER BY rating DESC ''', (chat_id,))

        user_data = cursor.fetchall()

        statistics_message = "Statistics for today in this chat:\n"

        if user_data:
            for data in user_data:
                first_name = data[0] if data[0] else ''  # Замінити None на порожній рядок
                last_name = data[1] if data[1] else ''  # Замінити None на порожній рядок
                rating = data[2]
                statistics_message += f"• {first_name + ' ' + last_name} :  {rating}★\n"
        else:
            statistics_message += "No statistics available for this chat."

        return statistics_message


def get_monthly_statistics(chat_id, month, year, chat_title):
    with sqlite3.connect(path.join(ROOT, "tg_bot_rating.db")) as db:
        cursor = db.cursor()

        cursor.execute(''' SELECT u.first_name, u.last_name, m.user_id, SUM(m.rating) AS total_rating
                       FROM users_ratings AS u
                       LEFT JOIN monthly_rating AS m ON u.id = m.user_id AND m.month = ? AND m.year = ?
                       WHERE u.chat_id = ?
                       GROUP BY u.id
                       ORDER BY total_rating DESC ''', (month, year, chat_id))

        user_data = cursor.fetchall()

        if user_data:
            statistics_for_month_message = f"Statistics for {month}-{year}:\n"
            for data in user_data:
                first_name = data[0] if data[0] else ''
                last_name = data[1] if data[1] else ''
                total_rating = data[3]
                statistics_for_month_message += f"• {first_name} {last_name}: {total_rating}★\n"

            return statistics_for_month_message

        return f"No statistics available for {month}-{year} in chat {chat_title}."
