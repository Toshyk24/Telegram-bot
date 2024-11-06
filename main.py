import os
import openai
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Получаем токены из переменных окружения
TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация OpenAI
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я ваш оппонент-бот с искусственным интеллектом. Задайте мне любой вопрос или возражение, и я постараюсь ответить."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    # Запрос к OpenAI API для генерации ответа
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Сыграй роль скептически настроенного клиента. Ответь на возражение: {user_message}",
        max_tokens=100,
        temperature=0.7
    )

    # Извлекаем текст ответа от модели
    ai_response = response.choices[0].text.strip()
    await update.message.reply_text(ai_response)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
