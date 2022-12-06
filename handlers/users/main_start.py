# - *- coding: utf- 8 - *-

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from config import main_photo
from filters.all_filters import IsUser
from keyboards import main_inline
from loader import dp, bot
from db_api import *
from utils.creation_msg import hello_msg


# Processing command "/start"
@dp.message_handler(text="⬅ На главную", state="*")
@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    username = message.from_user.username
    user = get_user(user_id=message.from_user.id)
    if user is None:
        add_user(user_id, username)
    await bot.send_photo(user_id, caption=hello_msg(username), photo=main_photo, reply_markup=main_inline())


@dp.message_handler(IsUser(), state="*")
@dp.callback_query_handler(IsUser(), state="*")
async def send_user_message(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id,
                           "<b>❗ Ваш профиль не был найден.</b>\n"
                           "▶ Введите /start")


@dp.message_handler(content_types=['photo'])
async def get_photo_id(message: types.Message):
    photo_id = message.photo[0].file_id
    print(photo_id)
