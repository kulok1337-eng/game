import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Токен вашего бота
TOKEN = "9123606264:AAEXd-sz5pL6KvSrSyKvG4tqSnGpKXSQEx4"

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    # Ссылка на ваше веб-приложение (Bothost сгенерирует её после деплоя index.html)
    # Замените https://your-app.bothost.app на адрес вашего сайта на Bothost
    web_app_url = os.getenv("WEBAPP_URL", "https://your-app.bothost.app")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть в Drag Nano Tower", web_app=WebAppInfo(url=web_app_url))]
    ])
    
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>! 💨\n\n"
        "Добро пожаловать в официальную мини-игру <b>Drag Nano Tower</b>.\n"
        "Укладывай поды ровно друг на друга, ставь рекорды и соревнуйся с друзьями!\n\n"
        "Нажми кнопку ниже, чтобы запустить игру:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    # Очищаем старые апдейты и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())