from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_inline():
    keyboard = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text="Hello!", callback_data="hello")
    keyboard.add(btn)
    return keyboard
