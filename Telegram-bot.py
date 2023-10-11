import telebot
import pymongo
from datetime import datetime
from pprint import pprint


TOKEN = "6326019480:AAETdZacx0o34VP9cbWyph4z6jan46Wcw-Q"
DATABASE_URL = "mongodb://localhost:27017/bot"


bot = telebot.TeleBot(TOKEN)


client = pymongo.MongoClient(DATABASE_URL)
db = client.bot


buttons = {
    "تحویل آیدی گروه": "/get_id",
    "حساب کاربری": "/user_account",
    "تسویه حساب": "/balance",
    "زیر مجموعه گیری": "/referral",
    "قوانین و مقررات": "/rules",
    "پشتیبانی سریع": "/support",
    "ما کی هستیم؟": "/about",
}


management_buttons = {
    "اطلاعات فرد و صفر کردن حساب کاربری": "/user_info",
    "آمار ربات": "/bot_stats",
    "استخراج آیدی های گروه از کانال هدف": "/extract_channel_ids",
}


def get_id(message):
    chat_id = message.chat.id
    user_id = message.from_user.id


    balance = get_balance(user_id)
    if balance < 10000:
        bot.send_message(chat_id, "موجودی شما کافی نیست. حداقل موجودی برای دریافت آیدی گروه 10000 تومان است.")
        return


    group_id = get_group_id(chat_id)


    bot.send_message(chat_id, f"آیدی گروه: {group_id}")

def user_account(message):
    chat_id = message.chat.id
    user_id = message.from_user.id


    user_info = get_user_info(user_id)


    bot.send_message(chat_id, f"نام: {user_info['name']}\nشناسه عددی: {user_info['id']}\nموجودی حساب: {user_info['balance']}\nتعداد زیر مجموعه ها: {user_info['referral_count']}\nتعداد آیدی های تحویل داده شده: {user_info['id_count']}")

def balance(message):
    chat_id = message.chat.id
    user_id = message.from_user.id


    balance = get_balance(user_id)



    bot.send_message(chat_id, f"موجودی حساب شما: {balance} تومان")

def referral(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Get the user's referral link

    referral_link = get_referral_link(user_id)


    bot.send_message(chat_id, f"لینک زیر مجموعه گیری شما: {referral_link}")

def rules(message):
    chat_id = message.chat.id


    rules = get_rules()


    bot.send_message(chat_id, rules)


def start(message):
    bot.send_message(message.chat.id, "سلام! این ربات ویکسل است.")
    bot.send_message(message.chat.id, "برای استفاده از ربات، لطفاً یکی از دکمه‌های زیر را انتخاب کنید.")
    for button in buttons:
        bot.send_message(message.chat.id, f"/<b>{button}</b> - {buttons[button]}")



def help(message):
    bot.send_message(message.chat.id, """این ربات یک ربات چند منظوره است که می تواند برای اهداف مختلفی استفاده شود. برخی از ویژگی های اصلی آن عبارتند از:

* تحویل آیدی گروه
* حساب کاربری
* تسویه حساب
* زیر مجموعه گیری
* قوانین و مقررات
* پشتیبانی سریع
* ما کی هستیم؟

برای کسب اطلاعات بیشتر، لطفاً از دکمه های زیر استفاده کنید.""")
