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
import openai 


class Reference:
    '''
    A class to store previously response from the chatGPT API
    '''

    def __init__(self) -> None:
        self.response = ""

load_dotenv()
openai.api_key = os.getenv("Open_API_KEY")

reference = Reference()

TOKEN = os.getenv("TOKEN")

#model name
MODEL_NAME = "gpt-4.1-mini"

#initialise bot
bot= Bot(token=TOKEN,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp= Dispatcher(storage=MemoryStorage())

def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response=""


@dp.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message):
    await message.reply(f"Hello, {message.from_user.full_name}! How can i assist you?")

@dp.message(Command(commands=["clear"]))
async def clear(message: types.Message):
    clear_past()
    await message.reply("I've deletetd the previous conversation and text")

@dp.message(Command(commands=["help"]))
async def help(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot!!! 
    /start - to start the conversaion
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :) :) :)
    """
    await message.reply(help_command)

@dp.message()
async def chatgpt(message: types.Message):
    print(f">>> USER: \n\t{message.text}")

    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": message.text}
        ]
    )

    reply = response.choices[0].message.content
    reference.response = reply  # Save the last response (optional)
    
    print(f">>> chatGPT: \n\t{reply}")
    await bot.send_message(chat_id=message.chat.id, text=reply)

async def main():
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
