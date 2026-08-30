import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
from bs4 import BeautifulSoup


BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция, которая идет на сайт ЦБ за курсом валют
async def get_rates():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json(content_type=None)
            usd = data["Valute"]["USD"]["Value"]
            eur = data["Valute"]["EUR"]["Value"]
            return f"💵 Доллар: {usd:.2f} руб.\n💶 Евро: {eur:.2f} руб."

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Напиши /rates чтобы узнать курс валют!")

@dp.message(Command("rates"))
async def rates_command(message: types.Message):
    text = await get_rates()
    await message.answer(text)

async def main():
    print("Ура! Бот успешно запущен и работает!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())