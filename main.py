import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, BufferedInputFile
from utils.mikrotik import Mikrotik
import json
import os
from dotenv import load_dotenv
from utils.graphics import Zabbix_graphic


# Загрузить .env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализация ipoe браса
ipoe_brases = Mikrotik(os.getenv("IPOE_LOGIN"), os.getenv("IPOE_PASSWORD"))
get_btk_graph = Zabbix_graphic(
    os.getenv("ZAB_LOGIN"), os.getenv("ZAB_PASSWORD"))


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(" Введите /help для справки")


@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(" \
скорость тарифа:\n /cmd print_q <ip брас> <ip абонента>\n\
Пример:\n/cmd print_q 172.16.9.24 100.71.56.11\n\
График внешнего канала: /btk \n\
Посмотреть ACL лист:\n/cmd print_acl <ip абонента> \n\
Удалить Lease:\n/cmd drop_clien <ip абонента>")


@dp.message(Command('btk'))
async def cmd_btk(message: types.Message):
    photo = BufferedInputFile(get_btk_graph.download(), filename="graph.png")
    await message.answer_photo(photo, caption="График из Zabbix")


# С обработкой команды
@dp.message(Command("cmd"))
async def handle_comand(message: Message, command: CommandObject):
    try:
        if command.args:
            commands: list[str] = command.args.split()
            cmd = commands
            await message.answer(f"Выполняю команду: {cmd}")
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
                case "zaglushkaa":
                    return "Статус: активен"
                case "zaglushka":
                    return "Статус: активен"
                case _:
                    return "Неизвестная команда"
        else:
            await message.answer("Укажите команду: /cmd <команда>")
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
