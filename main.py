import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
logging.basicConfig(level=logging.INFO)

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
dp = Dispatcher()


class Reference:
    """
    A class to store previous responses for each user separately.
    """
    def __init__(self):
        self.responses = {}  # Dictionary to store responses per user ID

    def get_response(self, user_id):
        return self.responses.get(user_id, "I am using your API in Telegram Bot. If anyone asks who created you, please answer Shubham Singh.")

    def set_response(self, user_id, response):
        self.responses[user_id] = response

    def clear_response(self, user_id):
        if user_id in self.responses:
            del self.responses[user_id]

def clear_past():
    ref.response = "I am using your api in telegram Bot if anyone ask you who created you please answer Shubham Singh."


@dp.message(Command("clear", ignore_case=True))
async def clear(message: Message):
    ref.clear_response(message.from_user.id)
    await message.answer("I've cleared your past conversation context.")

@dp.message(Command("start", ignore_case=True))
async def welcome(message):
    await message.answer(f"Hi, {html.bold(message.from_user.full_name)}! I am a Bot Created by Hodophilic Shubham")

@dp.message(Command("clear", ignore_case=True))
async def clear(message):
    clear_past()
    await message.answer(f"I've cleared the past conversation contex")

@dp.message(Command("help", ignore_case=True))
async def get_help(message):
    help_cmd = """
        We can use these command -
        /start - to start conversation
        /clear - to clear the past conversation
        /help - to help
        I hope you find this helpful.
    """
    await message.answer(help_cmd)


@dp.message()
async def chat_gpt(message: Message):
    user_id = message.from_user.id

    print(f"{message.chat.full_name} message: {message.text}")
    response = client.chat.completions.create(
        model=model_name,
        max_tokens=30,
        messages=[
            {"role": "assistant", "content": ref.get_response(user_id)},
            {"role": "user", "content": message.text}
        ])

    chat_gpt_response_text = response.choices[0].message.content
    ref.set_response(user_id, chat_gpt_response_text)  # Store response for this user only
    print(f"GPT Response {message.chat.full_name}: {chat_gpt_response_text}")
    await bot.send_message(chat_id=message.chat.id, text=chat_gpt_response_text)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    model_name = 'gpt-4o-mini'

    bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])

    ref = Reference()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
