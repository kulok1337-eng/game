import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# Токен вашего бота
TOKEN = "9123606264:AAEXd-sz5pL6KvSrSyKvG4tqSnGpKXSQEx4"

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    # Ваша реальная ссылка на веб-приложение
    web_app_url = "https://bot-1794770639-6069-efim111.bothost.tech"
    
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

# Веб-сервер для отдачи index.html (убирает Bad Gateway)
async def handle_index(request):
    return web.FileResponse('index.html')

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle_index)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    # Одновременно запускаем веб-сервер и телеграм-бота
    asyncio.create_task(web_server())
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())