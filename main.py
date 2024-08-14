import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import uuid


from click_on_button import click_on_button

logging.basicConfig(level=logging.INFO)
load_dotenv()
token = os.getenv('TOKEN')
dp = Dispatcher()

scheduler = AsyncIOScheduler()
job_id = f'my_job_{uuid.uuid4()}'

async def repeat_click_on_button(bot, chat_id):
    data = click_on_button()
    await bot.send_message(chat_id=chat_id, text=data)


async def main() -> None:
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    scheduler.start()
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    kb = [
        [KeyboardButton(text='START'), KeyboardButton(text='HELP'), KeyboardButton(text='STOP')],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply("Hello! Let's make an appointment", reply_markup=keyboard)


@dp.message(F.text.lower() == 'start')
async def start_bot(message: types.Message, bot: Bot):
    scheduler.add_job(repeat_click_on_button, 'interval', minutes=3, id=job_id, args=(bot, message.from_user.id))


@dp.message(F.text.lower() == 'help')
async def send_msg_help(message: types.Message):
    await message.reply(
        "This bot for check availability of appointment time for submitting documents "
        "to 'Pomorski Urząd Wojewódzki w Gdańsku'. "
        "For use this bot just click 'START'")


@dp.message(F.text.lower() == 'stop')
async def stop_bot(message: types.Message):
    scheduler.remove_job('my_job')
    await message.reply("Bot is stopped. For continuation, pleas, click 'START'")


@dp.message(F.text.lower() not in ['start', 'help', 'stop'])
async def send_msg_incorrect(message: types.Message):
    kb = [
        [KeyboardButton(text='START'), KeyboardButton(text='HELP'), KeyboardButton(text='STOP')],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply("Sorry, I didn't understand you. Let's try again", reply_markup=keyboard)


if __name__ == "__main__":
    asyncio.run(main())
