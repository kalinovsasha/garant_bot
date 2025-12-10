import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, BufferedInputFile
from utils.mikrotik import Mikrotik
import json
import os
from dotenv import load_dotenv
from utils.graphics import Zabbix_graphic
from db.users_db import Users_base

""" 
Команды на получение чата и имени
print(message.from_user.full_name)
print(message.from_user.id)
"""

# Загрузить .env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Создаем базу с пользователями
base = Users_base("./db/users.db")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализация ipoe браса
ipoe_brases = Mikrotik(os.getenv("IPOE_LOGIN"), os.getenv("IPOE_PASSWORD"))

get_btk_graph = Zabbix_graphic(
    os.getenv("ZAB_LOGIN"), os.getenv("ZAB_PASSWORD"), "btk")

get_lancache_graph = Zabbix_graphic(
    os.getenv("ZAB_LOGIN"), os.getenv("ZAB_PASSWORD"), "lancache")


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(" Введите /help для справки")


@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(" \
узнать свой id /tgid \n\
График внешнего канала: /btk \n\
График Lancache: /lancache \n\
скорость тарифа:\n /cmd print_q <ip брас> <ip абонента>\n\
Пример:\n/cmd print_q 172.16.9.24 100.71.56.11\n\
Посмотреть ACL лист:\n/cmd print_acl <ip абонента> \n\
Удалить Lease:\n/cmd drop_client <ip абонента>")


@dp.message(Command('btk'))
async def cmd_btk(message: types.Message):
    photo = BufferedInputFile(get_btk_graph.download(), filename="graph.png")
    await message.answer_photo(photo, caption="График BTK")


@dp.message(Command('lancache'))
async def cmd_lancache(message: types.Message):
    photo = BufferedInputFile(
        get_lancache_graph.download(), filename="graph.png")
    await message.answer_photo(photo, caption="График кеш steam")


# С обработкой команды
@dp.message(Command("cmd"))
async def handle_comand(message: Message, command: CommandObject):
    try:
        if command.args:
            commands: list[str] = command.args.split()
            await message.answer(f"Выполняю команду: {commands}")
            match commands[0]:
                # В commands[1] придет ip браса, в commands[2] ip абонента
                case "print_q":
                    print(f'{commands[1]}, {commands[2]}')
                    # Вывод информации о скорости
                    await message.answer(ipoe_brases.print_que(commands[1], commands[2]))
                # В commands[1] придет ip абонента
                case "print_acl":
                    await message.answer(ipoe_brases.print_acl(commands[1]))
                    return "Останавливаем процесс..."
                case "drop_client":
                    await message.answer(ipoe_brases.remove_lease_ip(commands[1]))
                # Секретная команда, делает анлим
                case "unlim":
                    await message.answer(ipoe_brases.set_unlim(commands[1]))
                case _:
                    await message.answer("Неверная команда")
        else:
            await message.answer("Укажите команду: /cmd <команда>")
    except Exception as e:
        print(e)


@dp.message(Command("tgid"))
async def get_tgid(message: Message, command: CommandObject):
    await message.answer(f"Name: {message.from_user.first_name} ID: {message.from_user.id} ")


@dp.message(Command("sys"))
async def get_sys(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Нет аргументов")
        return
    user = base.read_user(message.from_user.id)
    if user:
        if user[3] != 3: 
            await message.answer(f'Недостаточно прав для этой команды')
            return 
    cmd: list[str] = command.args.split()
    try:

        if cmd[0] == "add_user":
            if len(cmd) > 4:
                try:
                    await message.answer(f"ID: {cmd[1]},Name: {cmd[2]},ACCESS level: {cmd[3]},description: {cmd[4]}")
                    base.create_tguser(cmd[1], cmd[2], cmd[3], cmd[4])
                    user = base.read_user(cmd[1])
                    await message.answer(f"Пользователь добавлен: {user}")
                except Exception as e:
                    await message.answer(f"Не удалось добавить юзера, ошибка {e}")
            else:
                await message.answer(f"Должны быть данные ID ,Name ,ACCESS level ,description")

        if cmd[0] == "delete_user":
            try:
                base.delete_tguser(cmd[1])
                await message.answer(f"Удален пользователь c tg id{cmd[1]} ")
            except Exception as e:
                await message.answer(f"ошибка {e}")

        if cmd[0] == "show_users":
            try:
                users = base.read_users()
                await message.answer(f"Пользователи в базе:")
                for user in users:
                    await message.answer(f"{user}")
            except Exception as e:
                await message.answer(f"ошибка {e}")
    except Exception as e:
        print(e)


# Ответы на обычный текст
@dp.message()
async def mes(message: types.Message):
    text = message.text.lower()
    await message.answer(text)


async def main():
    print("Bot_started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
