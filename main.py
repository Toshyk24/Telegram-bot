from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '8191510937:AAEaJKNy0aIwNNPcE-XsIaV251z_cBxoVXc'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я бот для отработки возражений. Задай мне любой вопрос, и я помогу тебе отработать возражение.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    # Здесь будет логика для ответа на возражения
    response = "Ответ на возражение..."  # Примерный ответ на возражение
    await update.message.reply_text(response)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
