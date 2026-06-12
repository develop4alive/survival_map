from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from core.settings import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

basic_router_aiogram = Router()

def create_webapp_button() -> Optional[InlineKeyboardMarkup]:
    """Создает кнопку веб-приложения если настроен URL"""
    if not settings.bot.webapp_url:
        logger.warning("Webapp URL not configured")
        return None
        
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🌐 Открыть приложение",
                web_app=WebAppInfo(url=settings.bot.webapp_url))
        ]]
    )

@basic_router_aiogram.message(Command("start"))
async def handle_start(message: Message):
    """Обработчик команды /start"""
    user = message.from_user
    logger.info(f"Start command from user {user.id}, username={user.username}, first_name={user.first_name}")

    try:
        # Regular user greeting
        greeting = (
            "👋 Добро пожаловать! Мы рады что Вас заинтересовал наш сервис\n\n"
            "📝Не стоит воспринимать определение локаций за истину, ошибки геокодрования возможны, поэтому всегда проверяйте описание каждого события\n\n"
            "📍Бот не имеет обратной связи. Входящие сообщения не обрабатываются.\n"
            "🙈Дисклеймер!\n Мы не призываем к физической расправе над кем бы то ни было. Данное приложение это всего лишь систематизация и визуализация уже опубикованных постов с возможностью фильтрации событий по типу и по временным интервалам (для удобства)."
        )

        reply_markup = create_webapp_button()
        logger.info(f"Created webapp button for user {user.id}: {reply_markup is not None}")

        response = f"{greeting}\n\nИспользуйте кнопку ниже для доступа к приложению:"

        logger.info(f"Sending greeting to user {user.id}")
        await message.answer(response, reply_markup=reply_markup)
        logger.info(f"Successfully sent start message to user {user.id}")

    except Exception as e:
        logger.critical(f"Critical error in start handler: {e}", exc_info=True)
        await message.answer("⛔ Произошла внутренняя ошибка.")