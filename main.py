from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.i18n import SimpleI18n
import asyncio
import requests

# Тестовые токены
TELEGRAM_BOT_TOKEN = "7831746812:AAGjzXUiXhjBhEGJCDfOzd47TPxqvFd_kyI"
CRYPTOBOT_API_TOKEN = "329353:AAcI3b1HuARnkpyFLJ8hIy0beu7QKDTXMXx"

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN, session=AiohttpSession())
dp = Dispatcher()

# Создаем роутер для хэндлеров
router = Router()

# Обработчик команды /start
@router.message(commands=['start'])
async def start_handler(message: Message):
    await message.answer("Добро пожаловать! Для оплаты нажмите на кнопку ниже.", reply_markup=get_payment_button())

# Генерация кнопки оплаты
def get_payment_button():
    pay_url = create_invoice(amount=10.0, currency="USDT")  # Укажите сумму и валюту
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить через CryptoBot", url=pay_url)]
    ])
    return button

# Создание счета через API CryptoBot
def create_invoice(amount, currency):
    url = f"https://pay.crypt.bot/api/createInvoice"
    payload = {
        "token": CRYPTOBOT_API_TOKEN,
        "amount": amount,
        "currency": currency,
        "description": "Оплата тестового товара"
    }
    response = requests.post(url, json=payload).json()
    if response['ok']:
        return response['result']['pay_url']
    else:
        print("Ошибка при создании счета:", response)
        return None

# Основная функция
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
