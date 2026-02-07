import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Токен бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Список ID учителей (можно указать в .env файле как строку с разделением запятой)
TEACHER_IDS = list(map(int, os.getenv('TEACHER_IDS', '').split(','))) if os.getenv('TEACHER_IDS') else []

# Путь к базе данных
DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/bot_database.db')