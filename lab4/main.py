
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackContext,
    PicklePersistence
)
from config import TG_TOKEN, MODELS
from models import generate_response
from keyboards import (
    get_model_keyboard,
    get_main_menu_keyboard,
    get_filter_step_keyboard,
    remove_keyboard
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


CHOOSING_MODEL = 0
MAIN_MENU = 1
FREE_QUERY = 2
FILTER_BODY = 3
FILTER_CLASS = 4
FILTER_ENGINE = 5


BODY_TYPES = ["Седан", "Хэтчбек", "Кроссовер", "Универсал"]
CLASS_TYPES = ["Эконом", "Бизнес", "Премиум"]
ENGINE_TYPES = ["Бензин", "Дизель", "Электро"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для автомобильного подбора.\n"
        "Сначала выберите, к какой модели (LLM) мы будем обращаться:",
        reply_markup=get_model_keyboard()
    )
    return CHOOSING_MODEL

async def choose_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пользователь выбирает модель (Llama или GPT)."""
    model_name = update.message.text
    if model_name not in MODELS:
        await update.message.reply_text(
            "Пожалуйста, выберите модель из предложенных вариантов:",
            reply_markup=get_model_keyboard()
        )
        return CHOOSING_MODEL

    context.user_data["model_config"] = MODELS[model_name]

    await update.message.reply_text(
        f"Отлично! Вы выбрали модель «{model_name}».\n"
        "Теперь выберите режим автоподбора:",
        reply_markup=get_main_menu_keyboard()
    )
    return MAIN_MENU

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    choice = update.message.text

    if choice == "Подбор по запросу":
        await update.message.reply_text(
            "Опишите, что вы хотите подобрать.\n"
            "Например: «Нужна семейная машина для города», «Хочу спортивный седан» и т.д.",
            reply_markup=remove_keyboard()
        )
        return FREE_QUERY

    elif choice == "Подбор по фильтрам":
        await update.message.reply_text(
            "Выберите тип кузова:",
            reply_markup=get_filter_step_keyboard(BODY_TYPES)
        )
        return FILTER_BODY

    elif choice == "Назад в выбор модели":
        
        context.user_data.pop("model_config", None)
        await update.message.reply_text(
            "Выберите модель:",
            reply_markup=get_model_keyboard()
        )
        return CHOOSING_MODEL

    else:
        await update.message.reply_text(
            "Пожалуйста, воспользуйтесь кнопками ниже.",
            reply_markup=get_main_menu_keyboard()
        )
        return MAIN_MENU

async def handle_free_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if "model_config" not in context.user_data:
        await update.message.reply_text("❌ Сначала выберите модель через /start")
        return CHOOSING_MODEL

    user_text = update.message.text
    
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    try:
        response = await generate_response(
            model=context.user_data["model_config"],
            user_message=user_text
        )
        await update.message.reply_text(
            f"Результаты подбора:\n{response}\n\n"
            "Возвращаемся в главное меню.",
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

    
    await update.message.reply_text(
        "Выберите дальнейшее действие:",
        reply_markup=get_main_menu_keyboard()
    )
    return MAIN_MENU

async def filter_body_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пользователь выбрал тип кузова."""
    body_type = update.message.text
    if body_type == "Назад":
        await update.message.reply_text(
            "Возвращаемся в главное меню.",
            reply_markup=get_main_menu_keyboard()
        )
        return MAIN_MENU

    if body_type not in BODY_TYPES:
        await update.message.reply_text(
            "Пожалуйста, выберите тип кузова из списка или нажмите 'Назад'.",
            reply_markup=get_filter_step_keyboard(BODY_TYPES)
        )
        return FILTER_BODY

    context.user_data["body_type"] = body_type
    await update.message.reply_text(
        f"Вы выбрали кузов: {body_type}.\nТеперь выберите класс автомобиля:",
        reply_markup=get_filter_step_keyboard(CLASS_TYPES)
    )
    return FILTER_CLASS

async def filter_class_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    class_type = update.message.text
    if class_type == "Назад":
        await update.message.reply_text(
            "Выберите тип кузова:",
            reply_markup=get_filter_step_keyboard(BODY_TYPES)
        )
        return FILTER_BODY

    if class_type not in CLASS_TYPES:
        await update.message.reply_text(
            "Пожалуйста, выберите класс из списка или нажмите 'Назад'.",
            reply_markup=get_filter_step_keyboard(CLASS_TYPES)
        )
        return FILTER_CLASS

    context.user_data["class_type"] = class_type
    await update.message.reply_text(
        f"Вы выбрали класс: {class_type}.\nТеперь выберите тип двигателя:",
        reply_markup=get_filter_step_keyboard(ENGINE_TYPES)
    )
    return FILTER_ENGINE

async def filter_engine_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    engine_type = update.message.text
    if engine_type == "Назад":
        
        await update.message.reply_text(
            "Выберите класс автомобиля:",
            reply_markup=get_filter_step_keyboard(CLASS_TYPES)
        )
        return FILTER_CLASS

    if engine_type not in ENGINE_TYPES:
        await update.message.reply_text(
            "Пожалуйста, выберите тип двигателя из списка или нажмите 'Назад'.",
            reply_markup=get_filter_step_keyboard(ENGINE_TYPES)
        )
        return FILTER_ENGINE

    context.user_data["engine_type"] = engine_type

    
    body_type = context.user_data["body_type"]
    class_type = context.user_data["class_type"]
    engine_type = context.user_data["engine_type"]

    user_query = f"Нужен {body_type}, {class_type}, двигатель: {engine_type}"

    try:
        response = await generate_response(
            model=context.user_data["model_config"],
            user_message=user_query
        )
        await update.message.reply_text(
            f"По выбранным фильтрам:\n"
            f"• Кузов: {body_type}\n"
            f"• Класс: {class_type}\n"
            f"• Двигатель: {engine_type}\n\n"
            f"Результаты подбора:\n{response}",
            reply_markup=get_main_menu_keyboard()
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

    return MAIN_MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(
        "Диалог завершён. Введите /start, чтобы начать заново.",
        reply_markup=remove_keyboard()
    )
    return ConversationHandler.END

def main():
    
    application = ApplicationBuilder() \
        .token(TG_TOKEN) \
        .concurrent_updates(True) \
        .build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_MODEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, choose_model)
            ],
            MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)
            ],
            FREE_QUERY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_free_query)
            ],
            FILTER_BODY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, filter_body_handler)
            ],
            FILTER_CLASS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, filter_class_handler)
            ],
            FILTER_ENGINE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, filter_engine_handler)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
