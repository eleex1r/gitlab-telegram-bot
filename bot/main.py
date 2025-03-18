import logging
from telegram.ext import Application, CommandHandler
from config import TELEGRAM_BOT_TOKEN
from handlers import start, help_command

# Настраиваем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def main():
    # Создаём приложение бота
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Запускаем бота
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
