#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram-бот для обратной связи между учениками и учителями
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DATABASE_PATH
from bot.routers import setup_routers
from utils.database import DatabaseManager
from utils.keep_alive import KeepAliveService


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main():
    # Инициализация бота
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    
    # Инициализация хранилища FSM
    storage = MemoryStorage()
    
    # Инициализация диспетчера
    dp = Dispatcher(storage=storage)
    
    # Инициализация базы данных
    db = DatabaseManager(DATABASE_PATH)
    
    # Создание и запуск сервиса поддержания активности
    keep_alive_service = KeepAliveService(bot)
    keep_alive_service.start_service(interval=600)  # Пинг каждые 10 минут
    
    # Регистрация роутеров
    main_router = setup_routers()
    
    # Передача экземпляра базы данных в хендлеры
    dp.include_router(main_router)
    
    # Установка middleware для передачи базы данных в хендлеры
    async def db_middleware(handler, event, data):
        data["db"] = db
        return await handler(event, data)
    
    dp.update.middleware(db_middleware)
    
    print("Бот запущен и готов к работе!")
    
    # Запуск поллинга
    try:
        await dp.start_polling(bot)
    finally:
        # Остановка сервиса поддержания активности
        keep_alive_service.stop_service()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())