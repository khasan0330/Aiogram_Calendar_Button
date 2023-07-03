from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def generate_calendar_button():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text="Выбрать дату 📆")]
    ], resize_keyboard=True)
