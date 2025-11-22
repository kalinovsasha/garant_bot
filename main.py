import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from utils.mikrotik import Mikrotik
import json
import os
from dotenv import load_dotenv

# Загрузить .env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Задаем ипишники брасов
bras_servers = {
    "ipoe24": "172.16.9.24"
}


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("Ку")


# С обработкой команды
@dp.message(Command("cmd"))
async def handle_comand(message: Message, command: CommandObject):
    if command.args:
        cmd = command.args
        await message.answer(f"Выполняю команду: {cmd}")
    else:
        await message.answer("Укажите команду: /comand <команда>")

# Ответы на обычный текст


@dp.message()
async def mes(message: types.Message):
    text = message.text.lower()
    await message.answer(text)


async def main():
    print("Hello from garant-bot!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
