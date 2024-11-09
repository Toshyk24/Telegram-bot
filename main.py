import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Получаем токен из переменной окружения
TOKEN = os.getenv("TOKEN")

# Библиотека возражений для музыкальной школы
objections = {
    "price": [
        "Мне кажется, что это слишком дорого для меня.",
        "Я не уверен, стоит ли это своих денег.",
        "Есть ли у вас скидки для постоянных учеников?",
        "Если я захочу прекратить занятия, смогу ли я получить частичный возврат?"
    ],
    "results": [
        "Сколько времени потребуется, чтобы достичь первых результатов?",
        "Мне показалось, что на пробном занятии прогресс был медленным.",
        "Какой уровень я смогу достичь через полгода занятий?",
        "А смогу ли я самостоятельно практиковаться дома и видеть улучшения?"
    ],
    "teachers": [
        "А преподаватели у вас квалифицированные?",
        "Смогу ли я поменять преподавателя, если он мне не подойдет?",
        "Преподаватель на пробном занятии показался слишком молодым. Как мне понять, что он достаточно опытен?",
        "А преподаватели сами профессиональные музыканты?"
    ],
    "trial": [
        "Мне хотелось бы, чтобы занятия были более практическими.",
        "На пробном занятии было интересно, но я не понял, какой будет структура занятий.",
        "Какой метод обучения вы используете? Это традиционная методика или что-то современное?",
        "У меня были другие ожидания от пробного занятия."
    ],
    "schedule": [
        "А я могу сам выбирать дни и время для занятий?",
        "Что если мне нужно будет отменить или перенести урок?",
        "Если у меня возникнет перерыв на несколько недель, что с занятиями?",
        "Можно ли заморозить занятия, если мне нужно уехать?"
    ],
    "guarantee": [
        "Какую гарантию вы можете дать, что я достигну результата?",
        "Что будет, если мне не понравятся первые занятия?",
        "Могу ли я прекратить обучение без штрафов, если пойму, что это не мое?",
        "Если я не увижу прогресса, смогу ли я изменить программу обучения?"
    ]
}

# Ответы на успешные, нейтральные и неуспешные отработки возражений
positive_responses = [
    "Спасибо, теперь мне стало понятнее!",
    "Звучит убедительно, спасибо за объяснение!",
    "Теперь это выглядит куда более привлекательно!",
    "Хороший ответ! Это действительно меня убедило."
]

neutral_responses = [
    "Интересная мысль, но, возможно, есть что-то еще?",
    "Любопытный подход. А что еще можете добавить?",
    "Неплохо, но я все еще не до конца уверен.",
    "Звучит интересно, но мне нужно больше уверенности."
]

negative_responses = [
    "Мм, не совсем убедительно. Попробуйте ответить более подробно.",
    "Этого недостаточно, чтобы развеять мои сомнения.",
    "Мне все еще кажется, что это не стоит своих денег. Попробуйте еще раз.",
    "Не совсем то, что я хотел услышать. Возможно, попробуете что-то другое?"
]

# Ключевые слова для успешной отработки возражений по категориям
keywords = {
    "price": ["инвестиция", "качество", "ценность", "опыт", "гибкость"],
    "results": ["прогресс", "достижения", "успех", "цель", "регулярность"],
    "teachers": ["опыт", "квалификация", "музыкант", "профессионал", "подход"],
    "trial": ["структура", "методика", "обзор", "практика", "глубокий"],
    "schedule": ["гибкость", "удобно", "перенос", "заморозить", "регулярность"],
    "guarantee": ["гарантия", "уверенность", "возврат", "поддержка", "качество"]
}

# Функция для выбора случайного возражения из определенной категории
def get_random_objection():
    category = random.choice(list(objections.keys()))
    objection = random.choice(objections[category])
    return category, objection

# Функция для оценки ответа пользователя
def check_answer(user_message, category):
    # Проверяем, содержит ли ответ пользователя ключевые слова для данной категории
    if category in keywords:
        for keyword in keywords[category]:
            if keyword in user_message.lower():
                return "positive"
    # Проверяем на нейтральные слова, если нет ключевых
    if any(word in user_message.lower() for word in ["может", "возможно", "наверное", "стараемся"]):
        return "neutral"
    return "negative"

# Функция для выбора ответа в зависимости от оценки
def get_response(response_type):
    if response_type == "positive":
        return random.choice(positive_responses)
    elif response_type == "neutral":
        return random.choice(neutral_responses)
    else:
        return random.choice(negative_responses)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Бот начинает с предъявления возражения
    category, objection = get_random_objection()
    context.user_data['current_objection'] = category  # Сохраняем категорию возражения
    await update.message.reply_text(f"Ученик: {objection}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    category = context.user_data.get('current_objection', None)
    
    if category:
        # Проверка ответа пользователя и выбор типа реакции
        response_type = check_answer(user_message, category)
        response = get_response(response_type)

        # Если ответ успешный (positive), бот переходит к следующему возражению
        if response_type == "positive":
            new_category, new_objection = get_random_objection()
            context.user_data['current_objection'] = new_category
            await update.message.reply_text(f"{response}\n\nУченик: {new_objection}")
        else:
            # Если ответ нейтральный или негативный, бот просит дополнить
            await update.message.reply_text(response)
    else:
        # Если нет активного возражения, запускаем новое
        new_category, new_objection = get_random_objection()
        context.user_data['current_objection'] = new_category
        await update.message.reply_text(f"Ученик: {new_objection}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
