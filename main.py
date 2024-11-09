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

# Расширенные ключевые слова с добавлением различных форм
keywords = {
    "price": [
        "инвестиция", "инвестиции", "инвестиций", "инвестировать", "инвестирую", "инвестируем", 
        "качество", "качеством", "качественный", "качественная", "качественные", 
        "ценность", "ценности", "ценный", "ценная", "ценное", 
        "опыт", "опытом", "опытный", "опытная", "опытные",
        "гибкость", "гибкостью", "гибкий", "гибкая", "гибкие"
    ],
    "results": [
        "прогресс", "прогресса", "прогрессировать", "прогрессирую", "прогрессируем", 
        "достижение", "достижения", "достичь", "достигаю", "достигаем", 
        "успех", "успеха", "успешный", "успешно", 
        "цель", "цели", "целевой", 
        "регулярность", "регулярно", "регулярный", "регулярная"
    ],
    "teachers": [
        "опыт", "опыта", "опытный", "опытная", "опытные", 
        "квалификация", "квалификации", "квалифицированный", "квалифицированная", "квалифицированные", 
        "музыкант", "музыканты", "музыкантов", "музыкальный", "музыкальные", 
        "профессионал", "профессионалы", "профессиональный", "профессиональная", 
        "подход", "подхода", "подходящий", "подходящая"
    ],
    "trial": [
        "структура", "структуры", "структурный", 
        "методика", "методики", "методический", 
        "обзор", "обзора", "обзорный", 
        "практика", "практики", "практический", "практическая", "практичные", 
        "глубокий", "глубокая", "глубокое", "глубокие"
    ],
    "schedule": [
        "гибкость", "гибкости", "гибкий", "гибкая", "гибкие", 
        "удобно", "удобный", "удобная", "удобные", 
        "перенос", "переноса", "перенести", "переносим", "переношу", 
        "заморозить", "заморозка", "замораживаем", "заморозили", 
        "регулярность", "регулярно", "регулярный", "регулярная"
    ],
    "guarantee": [
        "гарантия", "гарантии", "гарантировать", "гарантируем", "гарантированно", 
        "уверенность", "уверенности", "уверенный", "уверенная", 
        "возврат", "возврата", "возвратный", "вернуть", "возвращаю", "возвращаем", 
        "поддержка", "поддержки", "поддерживать", "поддерживаю", "поддерживаем", 
        "качество", "качества", "качественный", "качественно"
    ]
}

# Функция для определения диапазона `required_score` по категории
def get_required_score_range(category):
    if category in ["price", "schedule"]:
        return random.randint(1, 3)  # Простые возражения
    elif category in ["results", "teachers", "trial", "guarantee"]:
        return random.randint(3, 5)  # Сложные возражения
    return 2  # Значение по умолчанию

# Функция для оценки ответа пользователя с системой баллов и проверкой длины
def check_answer(user_message, category):
    user_message = user_message.lower()
    score = 0
    required_score = get_required_score_range(category)  # Получаем случайное значение в диапазоне, зависящем от категории
    min_length = 30  # Минимальная длина ответа в символах

    if len(user_message) < min_length:
        return "negative"

    if category in keywords:
        for keyword in keywords[category]:
            if keyword in user_message:
                score += 1
                if score >= required_score:
                    return "positive"
    
    if score >= 1:
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

# Выбор случайного возражения
def get_random_objection():
    category = random.choice(list(objections.keys()))
    objection = random.choice(objections[category])
    return category, objection

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
