import os
import openai
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

    # Запрос к OpenAI API для генерации ответа с использованием нового Chat API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты скептически настроенный клиент, отвечай язвительно и остроумно на возражения."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=100,
        temperature=0.7
    )

    # Извлекаем текст ответа от модели
    ai_response = response['choices'][0]['message']['content']
    await update.message.reply_text(ai_response)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
