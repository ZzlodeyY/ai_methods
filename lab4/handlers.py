from typing import Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models import ModelManager

user_states: Dict[int, Dict[str, str]] = {}

async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Узнать функционал", callback_data="info")],
        [InlineKeyboardButton("Перейти к подбору", callback_data="start_selection")]
    ]
    await update.message.reply_text(
        "Добро пожаловать в авто-подбор! Выберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "info":
        keyboard = [[InlineKeyboardButton("Назад", callback_data="start")]]
        await query.edit_message_text(
            "Этот бот поможет вам подобрать автомобиль по запросу или фильтрам.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "start_selection":
        keyboard = [
            [InlineKeyboardButton("Подбор через запрос", callback_data="query_selection")],
            [InlineKeyboardButton("Подбор через фильтры", callback_data="filter_selection")],
            [InlineKeyboardButton("Назад", callback_data="start")]
        ]
        await query.edit_message_text(
            "Выберите способ подбора:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "query_selection":
        keyboard = [
            [InlineKeyboardButton("GPT-Neo", callback_data="text_model_gpt-neo")],
            [InlineKeyboardButton("LLaMA", callback_data="text_model_llama")],
            [InlineKeyboardButton("Назад", callback_data="start_selection")]
        ]
        await query.edit_message_text(
            "Выберите модель для обработки текстового запроса:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data.startswith("text_model_"):
        model_name = query.data.replace("text_model_", "")
        user_states[query.from_user.id] = {"model": model_name}
        await query.edit_message_text(
            f"Вы выбрали модель {model_name}. Введите ваш запрос для подбора автомобиля:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Назад", callback_data="query_selection")]
            ])
        )
    elif query.data == "filter_selection":
        keyboard = [
            [InlineKeyboardButton("GPT-Neo", callback_data="filter_model_gpt-neo")],
            [InlineKeyboardButton("LLaMA", callback_data="filter_model_llama")],
            [InlineKeyboardButton("Назад", callback_data="start_selection")]
        ]
        await query.edit_message_text(
            "Выберите модель для обработки подбора по фильтрам:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data.startswith("filter_model_"):
        model_name = query.data.replace("filter_model_", "")
        user_states[query.from_user.id] = {
            "model": model_name,
            "filters": ""
        }
        keyboard = [
            [InlineKeyboardButton("Эконом", callback_data="class_эконом"),
             InlineKeyboardButton("Бизнес", callback_data="class_бизнес"),
             InlineKeyboardButton("Премиум", callback_data="class_премиум")],
            [InlineKeyboardButton("Назад", callback_data="filter_selection")]
        ]
        await query.edit_message_text(
            "Выберите класс автомобиля:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data.startswith("class_"):
        car_class = query.data.replace("class_", "")
        user_states[query.from_user.id]["filters"] = f"Класс: {car_class}"
        keyboard = [
            [InlineKeyboardButton("Седан", callback_data="body_седан"),
             InlineKeyboardButton("Хэтчбек", callback_data="body_хэтчбек"),
             InlineKeyboardButton("Кроссовер", callback_data="body_кроссовер"),
             InlineKeyboardButton("Купе", callback_data="body_купе"),
             InlineKeyboardButton("Универсал", callback_data="body_универсал")],
            [InlineKeyboardButton("Назад", callback_data="filter_selection")]
        ]
        await query.edit_message_text(
            "Выберите тип кузова:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data.startswith("body_"):
        body_type = query.data.replace("body_", "")
        user_states[query.from_user.id]["filters"] += f", Тип кузова: {body_type}"
        keyboard = [
            [InlineKeyboardButton("Электро", callback_data="engine_электро"),
             InlineKeyboardButton("Гибрид", callback_data="engine_гибрид"),
             InlineKeyboardButton("Бензин", callback_data="engine_бензин"),
             InlineKeyboardButton("Дизель", callback_data="engine_дизель")],
            [InlineKeyboardButton("Назад", callback_data="filter_selection")]
        ]
        await query.edit_message_text(
            "Выберите тип двигателя:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data.startswith("engine_"):
        engine_type = query.data.replace("engine_", "")
        user_states[query.from_user.id]["filters"] += f", Двигатель: {engine_type}"
        filters_summary = user_states[query.from_user.id]["filters"]
        model_manager = ModelManager.get_instance()
        response = await model_manager.generate_response(
            user_states[query.from_user.id]["model"], 
            f"Подбери автомобиль со следующими параметрами: {filters_summary}"
        )
        response = response or "Не удалось сгенерировать подборку. Попробуйте еще раз."
        await query.edit_message_text(
            f"Подборка на основе параметров: {filters_summary}\n\n{response}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Новый подбор", callback_data="start_selection")]
            ])
        )

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_states or "model" not in user_states[user_id]:
        await update.message.reply_text(
            "Пожалуйста, выберите модель или способ подбора."
        )
        return

    model = user_states[user_id]["model"]
    prompt = update.message.text
    model_manager = ModelManager.get_instance()
    response = await model_manager.generate_response(model, prompt)
    response = response or "Не удалось сгенерировать подборку. Попробуйте еще раз."
    await update.message.reply_text(
        f"Подборка автомобилей по вашему запросу:\n\n{response}"
    )
