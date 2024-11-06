from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import random

TOKEN = os.getenv("TOKEN")

# База возражений и ответов с язвительными комментариями
responses = {
    "дорого": [
        "Хм, а вы уверены, что готовы инвестировать в свое развитие? Качественные знания требуют вложений.",
        "Цена — это показатель качества. Или вы ищете самый дешевый вариант без гарантии результата?",
        "Дорого по сравнению с чем? Наши услуги стоят своих денег, ведь вы получаете знания от профессионалов."
    ],
    "качество": [
        "Ну, качество — это наше кредо. У нас все преподаватели с опытом и страстью к своему делу. Сомневаетесь?",
        "А вы много где обучались, чтобы оценивать качество? Попробуйте наши уроки и убедитесь сами.",
        "Если для вас важны результаты, у нас отличный трек рекорд по ученикам. Но, конечно, всегда есть место для улучшений."
    ],
    "результаты": [
        "Многие из наших учеников достигли успехов, но ведь результат еще зависит и от ученика, верно?",
        "Интересуетесь результатами? Может быть, просто стоит попробовать и самому оценить?",
        "Мы ориентируемся на результат, но ведь и вы должны приложить усилия. Или вы ищете мгновенную магию?"
    ],
    "возврат": [
        "Возврат? Мы уверены в своих услугах. Может, сначала попробуем урок, а потом уже будем говорить о возвратах?",
        "О, так вы сразу настроены на возврат? Не слишком ли пессимистично?",
        "Если не понравится, мы готовы обсудить возврат, но такие случаи у нас редкость. Уверены, что все пройдет гладко."
    ]
}

# Функция для выбора случайного ответа
def get_response(keyword):
    return random.choice(responses[keyword])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я ваш оппонент-бот, готовый обсудить любые возражения. Давайте попробуем!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()
    response = "Хм, интересная точка зрения, но можете уточнить?"

    # Проверка на ключевые слова и выбор язвительного ответа
    for keyword in responses:
        if keyword in user_message:
            response = get_response(keyword)
            break

    await update.message.reply_text(response)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
