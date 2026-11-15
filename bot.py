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

# Веб-сервер с абсолютным путем к index.html
async def handle_index(request):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'index.html')
    
    if os.path.exists(file_path):
        return web.FileResponse(file_path)
    else:
        return web.Response(text="ERROR: index.html not found on server!", status=404)

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
    
    # Запускаем веб-сервер и бота
    asyncio.create_task(web_server())
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())