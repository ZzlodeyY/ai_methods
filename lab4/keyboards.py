
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

def get_model_keyboard():
    """Клавиатура для выбора одной из двух моделей."""
    keyboard = [
        ["Llama"],
        ["GPT"]
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

def get_main_menu_keyboard():
    """Главное меню бота: выбор способа автоподбора."""
    keyboard = [
        ["Подбор по запросу"],
        ["Подбор по фильтрам"],
        ["Назад в выбор модели"]
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

def get_filter_step_keyboard(options):
    """Клавиатура для пошагового выбора (кузов, класс, двигатель)."""
    return ReplyKeyboardMarkup(
        [[opt] for opt in options] + [["Назад"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )

def remove_keyboard():
    """Удаляет клавиатуру."""
    return ReplyKeyboardRemove()
