# ===============================
# QR CODE BOT 1-QISM A
# ===============================

import telebot
import qrcode
import os
from datetime import datetime
from telebot import types


# ===============================
# SOZLAMALAR
# ===============================

TOKEN = "8370617478:AAHSzoSM401p7v0i6ioSI7R7laaok-Wn5L0"
ADMIN_ID = 7600986332   # o'zingizni Telegram ID yozing

bot = telebot.TeleBot(TOKEN)


# ===============================
# DATABASE USERS.TXT
# ===============================

FILE = "users.txt"


def create_file():
    if not os.path.exists(FILE):
        open(FILE, "w", encoding="utf-8").close()


create_file()


# FORMAT:

# id|ism|username|telefon|balans|spent|qr|status|date


def get_users():

    users = []

    with open(FILE, "r", encoding="utf-8") as f:

        for line in f:

            line=line.strip()

            if line:

                data=line.split("|")

                users.append(data)

    return users



def save_users(users):

    with open(FILE,"w",encoding="utf-8") as f:

        for u in users:

            f.write("|".join(u)+"\n")



def find_user(uid):

    users=get_users()

    for u in users:

        if u[0]==str(uid):

            return u

    return None



def add_user(user):

    users=get_users()

    users.append(user)

    save_users(users)



def update_user(user):

    users=get_users()

    for i,u in enumerate(users):

        if u[0]==user[0]:

            users[i]=user

    save_users(users)



# ===============================
# KLAVIATURA
# ===============================


def main_menu():

    kb=types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    kb.row(
        "📱 QR yaratish",
        "👤 Profil"
    )

    kb.row(
        "💰 Hisobim",
        "💳 Hisob to'ldirish"
    )

    kb.row(
        "📊 Statistika",
        "ℹ️ Yordam"
    )

    return kb



def admin_menu():

    kb=types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    kb.row(
        "📊 Admin statistika",
        "👥 Mijozlar"
    )

    kb.row(
        "💰 Pul qo'shish",
        "➖ Pul olish"
    )

    kb.row(
        "🎁 Bonus",
        "🚫 Bloklash"
    )

    kb.row(
        "📢 Reklama"

    )

    return kb



# ===============================
# START
# ===============================


@bot.message_handler(commands=["start"])
def start(message):

    uid=message.from_user.id

    user=find_user(uid)


    if not user:


        new=[

            str(uid),

            message.from_user.first_name or "NoName",

            "@"+message.from_user.username 
            if message.from_user.username 
            else "None",

            "0",

            "0",

            "0",

            "active",

            str(datetime.now().date())

        ]


        add_user(new)


        bot.send_message(
            uid,
            "🎉 Xush kelibsiz!\n\n"
            "QR Code yaratish botiga xush kelibsiz.",
            reply_markup=main_menu()
        )


    else:

        bot.send_message(
            uid,
            "👋 Qaytganingiz bilan!",
            reply_markup=main_menu()
        )



# ===============================
# PROFIL
# ===============================


@bot.message_handler(func=lambda m:m.text=="👤 Profil")
def profile(message):

    user=find_user(message.from_user.id)


    if user:

        text=f"""
👤 Profil

🆔 ID:
{user[0]}

👨 Ism:
{user[1]}

Username:
{user[2]}

💰 Balans:
{user[4]} so'm

📱 QR soni:
{user[6]}

📅 Sana:
{user[8]}
"""

        bot.send_message(
            message.chat.id,
            text
        )



# ===============================
# HISOBIM
# ===============================


@bot.message_handler(func=lambda m:m.text=="💰 Hisobim")
def balance(message):

    user=find_user(message.from_user.id)


    bot.send_message(
        message.chat.id,
        f"""
💰 Hisobingiz

Balans:
{user[4]} so'm

Ishlatilgan:
{user[5]} so'm
"""
    )



# ===============================
# ADMIN KIRISH
# ===============================


@bot.message_handler(commands=["admin"])
def admin(message):

    if message.from_user.id==ADMIN_ID:

        bot.send_message(
            message.chat.id,
            "👑 Admin panel",
            reply_markup=admin_menu()
        )

    else:

        bot.send_message(
            message.chat.id,
            "❌ Siz admin emassiz"
        )



print("BOT ISHGA TUSHDI")


bot.infinity_polling()
# ===============================
# 2-QISM QR CODE SISTEMA
# ===============================


def create_qr(data, name):

    path=f"{name}.png"

    img=qrcode.make(data)

    img.save(path)

    return path



# ===============================
# QR MENU
# ===============================


@bot.message_handler(func=lambda m:m.text=="📱 QR yaratish")
def qr_menu(message):

    kb=types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    kb.row(
        "🔗 Link QR",
        "☎ Telefon QR"
    )

    kb.row(
        "📝 Matn QR",
        "📶 WiFi QR"
    )

    kb.row(
        "📍 Lokatsiya QR",
        "⬅️ Orqaga"
    )


    bot.send_message(
        message.chat.id,
        "QR turini tanlang:",
        reply_markup=kb
    )



# ===============================
# LINK QR
# ===============================


@bot.message_handler(func=lambda m:m.text=="🔗 Link QR")
def link_qr(message):

    msg=bot.send_message(
        message.chat.id,
        "🔗 Link yuboring:"
    )

    bot.register_next_step_handler(
        msg,
        make_link_qr
    )


def make_link_qr(message):

    file=create_qr(
        message.text,
        "link_qr"
    )


    bot.send_photo(
        message.chat.id,
        open(file,"rb"),
        caption="✅ Link QR tayyor"
    )


    os.remove(file)



# ===============================
# TELEFON QR
# ===============================


@bot.message_handler(func=lambda m:m.text=="☎ Telefon QR")
def phone_qr(message):

    msg=bot.send_message(
        message.chat.id,
        "☎ Telefon raqam yuboring:"
    )


    bot.register_next_step_handler(
        msg,
        make_phone_qr
    )



def make_phone_qr(message):

    data="tel:"+message.text


    file=create_qr(
        data,
        "phone_qr"
    )


    bot.send_photo(
        message.chat.id,
        open(file,"rb"),
        caption="✅ Telefon QR tayyor"
    )


    os.remove(file)



# ===============================
# MATN QR
# ===============================


@bot.message_handler(func=lambda m:m.text=="📝 Matn QR")
def text_qr(message):

    msg=bot.send_message(
        message.chat.id,
        "📝 Matn yozing:"
    )


    bot.register_next_step_handler(
        msg,
        make_text_qr
    )



def make_text_qr(message):


    file=create_qr(
        message.text,
        "text_qr"
    )


    bot.send_photo(
        message.chat.id,
        open(file,"rb"),
        caption="✅ Matn QR tayyor"
    )


    os.remove(file)




# ===============================
# WIFI QR
# ===============================


@bot.message_handler(func=lambda m:m.text=="📶 WiFi QR")
def wifi_qr(message):

    msg=bot.send_message(
        message.chat.id,
        """
📶 WiFi ma'lumotlarini yuboring:

Format:

SSID|PASSWORD

Misol:

Wifi123|12345678
"""
    )


    bot.register_next_step_handler(
        msg,
        make_wifi_qr
    )



def make_wifi_qr(message):


    data=message.text.split("|")


    if len(data)!=2:

        bot.send_message(
            message.chat.id,
            "❌ Format xato"
        )

        return


    wifi=f"WIFI:T:WPA;S:{data[0]};P:{data[1]};;"


    file=create_qr(
        wifi,
        "wifi_qr"
    )


    bot.send_photo(
        message.chat.id,
        open(file,"rb"),
        caption="✅ WiFi QR tayyor"
    )


    os.remove(file)



# ===============================
# LOKATSIYA QR
# ===============================


@bot.message_handler(func=lambda m:m.text=="📍 Lokatsiya QR")
def location_qr(message):

    msg=bot.send_message(
        message.chat.id,
        """
📍 Lokatsiya yuboring

Format:

latitude,longitude

Misol:

41.3111,69.2797
"""
    )


    bot.register_next_step_handler(
        msg,
        make_location_qr
    )



def make_location_qr(message):


    loc=message.text.split(",")


    if len(loc)!=2:

        bot.send_message(
            message.chat.id,
            "❌ Format xato"
        )

        return



    data=f"https://maps.google.com/?q={loc[0]},{loc[1]}"


    file=create_qr(
        data,
        "location_qr"
    )


    bot.send_photo(
        message.chat.id,
        open(file,"rb"),
        caption="✅ Lokatsiya QR tayyor"
    )


    os.remove(file)




# ===============================
# ORQAGA
# ===============================


@bot.message_handler(func=lambda m:m.text=="⬅️ Orqaga")
def back(message):

    bot.send_message(
        message.chat.id,
        "Asosiy menyu",
        reply_markup=main_menu()
    )
    # ===============================
# 3-QISM HISOB TO'LDIRISH
# ===============================


# vaqtinchalik to'lov saqlash
payments = {}



# ===============================
# HISOB TO'LDIRISH
# ===============================


@bot.message_handler(func=lambda m:m.text=="💳 Hisob to'ldirish")
def add_balance(message):

    bot.send_message(
        message.chat.id,
        """
💳 Hisob to'ldirish

To'lovni amalga oshiring.

To'lov qilganingizdan keyin:
- chek rasmini yuboring
- yoki to'lov skrinshotini yuboring

Admin tekshiradi.

⏳ Admin 3 soat ichida javob beradi.
"""
    )

    bot.register_next_step_handler(
        message,
        get_payment
    )



# ===============================
# CHEK QABUL QILISH
# ===============================


def get_payment(message):

    uid=message.from_user.id


    payments[uid]={
        "user":uid,
        "message_id":message.message_id
    }



    if message.photo:


        file_id=message.photo[-1].file_id


        payments[uid]["photo"]=file_id



        user=find_user(uid)



        text=f"""
🔔 Yangi to'lov so'rovi

👤 Ism:
{user[1]}

🆔 ID:
{user[0]}

Username:
{user[2]}

📌 Tekshirish kerak.
"""


        kb=types.InlineKeyboardMarkup()


        kb.add(
            types.InlineKeyboardButton(
                "✅ Tasdiqlash",
                callback_data=f"pay_yes_{uid}"
            )
        )


        kb.add(
            types.InlineKeyboardButton(
                "❌ Rad qilish",
                callback_data=f"pay_no_{uid}"
            )
        )


        bot.send_photo(
            ADMIN_ID,
            file_id,
            caption=text,
            reply_markup=kb
        )


    else:


        bot.send_message(
            message.chat.id,
            "❌ Iltimos chek rasmini yuboring."
        )

        return



    bot.send_message(
        message.chat.id,
        """
✅ Chek qabul qilindi.

Admin tekshiradi.

⏳ 3 soat ichida javob beriladi.
"""
    )



# ===============================
# ADMIN TO'LOV JAVOBI
# ===============================


@bot.callback_query_handler(
    func=lambda call:
    call.data.startswith("pay_")
)
def payment_answer(call):


    data=call.data.split("_")


    action=data[1]

    uid=int(data[2])



    if call.from_user.id!=ADMIN_ID:

        return



    user=find_user(uid)



    if action=="yes":


        # default summa
        # keyin admin paneldan o'zgartiramiz


        user[4]=str(
            int(user[4])+10000
        )


        update_user(user)



        bot.send_message(
            uid,
            """
✅ To'lov tasdiqlandi.

💰 Hisobingizga 10000 so'm qo'shildi.
"""
        )


        bot.answer_callback_query(
            call.id,
            "Tasdiqlandi"
        )



    elif action=="no":


        bot.send_message(
            uid,
            """
❌ To'lov rad qilindi.

Qaytadan yuborishingiz mumkin.
"""
        )


        bot.answer_callback_query(
            call.id,
            "Rad qilindi"
        )



# ===============================
# ADMIN PUL BERISH FUNKSIYA
# KEYINGI QISMDA TO'LIQ PANELGA ULANADI
# ===============================
