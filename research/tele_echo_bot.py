import logging
import asyncio
from aiogram import Bot, Dispatcher , types
from dotenv import load_dotenv
import os
from aiogram.filters import Command

from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

load_dotenv() 
API_TOKEN=os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

#initialise bot
bot= Bot(token=API_TOKEN,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp= Dispatcher(storage=MemoryStorage())

@dp.message(Command(commands=["start", "help"]))
async def command_start_handler(message: types.Message):
    await message.reply(f"Hello, {message.from_user.full_name}!")

@dp.message()
async def echo_handler(message: Message):
    
    await message.answer(message.text)

async def main():
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())