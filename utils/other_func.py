import datetime
from aiogram import Dispatcher, types
from config import admins
from loader import bot


# start up notification
async def on_startup_notify(dp: Dispatcher):
    await send_all_admin(f"<b>✅ Бот был успешно запущен</b>\n")


# mailing to all admins
async def send_all_admin(message, markup=None, not_me=0):
    if markup is None:
        for admin in admins:
            try:
                if str(admin) != str(not_me):
                    await bot.send_message(admin, message, disable_web_page_preview=True)
            except:
                pass
    else:
        for admin in admins:
            try:
                if str(admin) != str(not_me):
                    await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
            except:
                pass


def clear_firstname(firstname):
    if "<" in firstname: firstname = firstname.replace("<", "*")
    if ">" in firstname: firstname = firstname.replace(">", "*")
    return firstname


# commands registration
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота 🔥")
    ])
