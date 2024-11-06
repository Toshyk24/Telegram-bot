import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Получаем токен из переменной окружения
TOKEN = os.getenv("TOKEN")

# Список возражений
objections = [
    "Это слишком дорого для меня.",
    "Я не уверен в качестве обучения.",
    "А будут ли результаты после этих уроков?",
    "Что, если мне не понравится? Можно ли вернуть деньги?",
    "У вас есть опытные преподаватели?",
]

# Ответы бота на успешную и неуспешную отработку возражений
positive_responses = [
    "Хороший ответ! Это действительно меня убедило.",
    "Вы меня убедили, теперь это звучит гораздо лучше!",
    "Отлично, теперь я понимаю, что это стоит своих денег.",
]

negative_responses = [
    "Мм, не совсем убедительно. Попробуйте ответить более подробно.",
    "Этого недостаточно, чтобы развеять мои сомнения.",
    "Мне все еще кажется, что это не стоит своих денег. Попробуйте еще раз."
]

# Ключевые слова для определения успешной отработки возражений
keywords = {
    "дорого": ["инвестиция", "качество", "опыт"],
    "качество": ["профессионал", "опыт", "подход"],
    "результаты": ["достижения", "успех", "поддержка"],
    "возврат": ["гарантия", "возврат", "безопасность"],
    "преподаватели": ["опыт", "сертификация", "квалификация"]
}

# Функция для выбора случайного возражения
def get_random_objection():
    return random.choice(objections)

# Функция для проверки ответа пользователя
def check_answer(user_message, objection):
    for keyword in keywords:
        if keyword in objection.lower():
            # Проверяем, содержит ли ответ пользователя нужные ключевые слова
            for kw in keywords[keyword]:
                if kw in user_message.lower():
                    return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Бот начинает с предъявления возражения
    objection = get_random_objection()
    context.user_data['current_objection'] = objection  # Сохраняем текущее возражение
    await update.message.reply_text(f"Клиент: {objection}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    objection = context.user_data.get('current_objection', None)
    
    if objection:
        # Проверяем ответ пользователя
        if check_answer(user_message, objection):
            response = random.choice(positive_responses)
            # Смена на новое возражение
            new_objection = get_random_objection()
            context.user_data['current_objection'] = new_objection
            await update.message.reply_text(f"{response}\n\nКлиент: {new_objection}")
        else:
            # Отправляем негативный ответ и просим уточнить
            response = random.choice(negative_responses)
            await update.message.reply_text(response)
    else:
        # Если нет активного возражения, просто запускаем новое
        new_objection = get_random_objection()
        context.user_data['current_objection'] = new_objection
        await update.message.reply_text(f"Клиент: {new_objection}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
