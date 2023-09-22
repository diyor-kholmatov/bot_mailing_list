import asyncio

from aiogram import Bot, Dispatcher, executor, types

from config import token, admin_id
from getting_id import joinedUsers, joinedFile


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start", state=None)

async def welcome(message):
    joinedFile = open("joined.txt", "r")
    joinedUsers = set()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("joined.txt", "a", encoding="utf-8")
        joinedFile.write(str(message.chat.id)+(message.from_user.first_name)+ "\n")
        joinedUsers.add(message.chat.id)

    await bot.send_message(message.chat.id, f"ПРИВЕТ, *{message.from_user.first_name},* БОТ РАБОТАЕТ\n"
                                            f"Чтобы отпрваить сообщение введи команду /send\n"
                                            f"Чтобы увидеть кто посмотрел сообщение введи команду /show")

@dp.message_handler(commands='show')
async def show_users(message: types.Message):
    await message.answer(f"Users\n"
                         f"*{joinedUsers}*", parse_mode='Markdown')

@dp.message_handler(commands='send')
async def sender(message):
    if message.chat.id == admin_id:
        await bot.send_message(message.chat.id, f"*Рассылка началась \nБот оповестит когда рассылку закончит*", parse_mode='Markdown')
        receive_users, block_users = 0, 0
        joinedFile = open("joined.txt", "r")
        jionedUsers = set()
        for line in joinedFile:
            jionedUsers.add(line.strip())
        joinedFile.close()
        for user in jionedUsers:
            try:
                await bot.send_message(user, message.text[message.text.find(' '):])
                receive_users += 1
            except:
                block_users += 1
            await asyncio.sleep(0.4)
        await bot.send_message(message.chat.id, f"*Рассылка была завершена *\n"
                                                              f"получили сообщение: *{receive_users}*\n"
                                                               f"заблокировали бота: *{block_users}*", parse_mode='Markdown')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp)