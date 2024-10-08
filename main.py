import asyncio
import logging
import os
import uuid

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from click_on_button import click_on_button

logging.basicConfig(level=logging.INFO)
load_dotenv()
token = os.getenv('TOKEN')
dp = Dispatcher()
scheduler = AsyncIOScheduler()

user_jobs = {}


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
    # Генерация уникального job_id для каждого пользователя
    job_id = f"my_job_{message.from_user.id}_{uuid.uuid4()}"
    
    # Сохранение job_id в словарь
    user_jobs[message.from_user.id] = job_id
    scheduler.add_job(repeat_click_on_button, 'interval', minutes=30, id=job_id, args=(bot, message.from_user.id))
    await message.reply("Bot started! It will check every 30 minutes.")


@dp.message(F.text.lower() == 'help')
async def send_msg_help(message: types.Message):
    await message.reply(
        "This bot for check availability of appointment time for submitting documents "
        "to 'Pomorskim Urzędzie Wojewódzkim w Gdańsku'. "
        "For use this bot just click 'START'")


@dp.message(F.text.lower() == 'stop')
async def stop_bot(message: types.Message):
    job_id = user_jobs.get(message.from_user.id)
    
    if job_id:
        scheduler.remove_job(job_id)
        await message.reply("Bot is stopped. For continuation, please, click 'START'")
        # Удаляем job_id из словаря
        del user_jobs[message.from_user.id]
    else:
        await message.reply("No active job found. Please start the bot first.")

@dp.message(lambda message: message.text.lower() not in ['start', 'help', 'stop'])
async def send_msg_about_incorrect_msg(message: types.Message):
    kb = [
        [KeyboardButton(text='START'), KeyboardButton(text='HELP'), KeyboardButton(text='STOP')],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply("Sorry, i did not understand you:( Let's try again. Choose one of the buttons below",
                        reply_markup=keyboard)


if __name__ == "__main__":
    asyncio.run(main())
