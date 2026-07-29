import os
import sqlite3
import telebot
import qrcode

from telebot import types


TOKEN = os.getenv("8370617478:AAHwWZRiyF72El1A_IOYpGXI2gicChcpe-c")

ADMIN_ID = 7600986332

QR_PRICE = 150


bot = telebot.TeleBot(TOKEN)



# ================= DATABASE =================

db = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT,
    name TEXT,
    phone TEXT,
    balance INTEGER DEFAULT 1000,
    spent INTEGER DEFAULT 0,
    qr_count INTEGER DEFAULT 0
)
""")


db.commit()



def add_user(message):

    uid = message.from_user.id

    cursor.execute(
        "SELECT id FROM users WHERE id=?",
        (uid,)
    )

    result = cursor.fetchone()


    if not result:

        cursor.execute(
            """
            INSERT INTO users
            (id,username,name,balance)
            VALUES(?,?,?,?)
            """,
            (
                uid,
                message.from_user.username,
                message.from_user.first_name,
                1000
            )
        )

        db.commit()



def get_user(uid):

    cursor.execute(
        "SELECT * FROM users WHERE id=?",
        (uid,)
    )

    return cursor.fetchone()



def update_user(uid,balance,spent,qr):

    cursor.execute(
        """
        UPDATE users
        SET balance=?,
        spent=?,
        qr_count=?
        WHERE id=?
        """,
        (
            balance,
            spent,
            qr,
            uid
        )
    )

    db.commit()



# ================= MENULAR =================


def main_menu():

    menu = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )


    menu.add(
        "🌐 Link",
        "📝 Matn"
    )


    menu.add(
        "📞 Telefon",
        "📧 Email"
    )


    menu.add(
        "📶 Wi-Fi"
    )


    menu.add(
        "💳 Hisobim"
    )


    menu.add(
        "📱 Raqam yuborish"
    )


    return menu



def admin_menu():

    menu = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )


    menu.add(
        "📊 Statistika",
        "💰 Pul berish"
    )


    menu.add(
        "🎁 Bonus"
    )


    menu.add(
        "🚫 Bloklash",
        "✅ Ochish"
    )


    menu.add(
        "🚪 Chiqish"
    )


    return menu



# vaqtinchalik holatlar

user_mode = {}

blocked = set()



# ================= START =================


@bot.message_handler(commands=["start"])
def start(message):

    add_user(message)


    uid = message.from_user.id


    if uid in blocked:

        bot.send_message(
            uid,
            "🚫 Siz bloklangansiz"
        )

        return



    if uid == ADMIN_ID:

        bot.send_message(
            uid,
            "👑 Admin panel",
            reply_markup=admin_menu()
        )

    else:

        bot.send_message(
            uid,
            """
🤖 QR CODE BOT

💰 Boshlang'ich balans: 1000 so'm

Har bir QR:
150 so'm
""",
            reply_markup=main_menu()
        )



# ================= ADMIN =================


@bot.message_handler(commands=["admin"])
def admin(message):

    if message.from_user.id == ADMIN_ID:

        bot.send_message(
            message.chat.id,
            "👑 Admin panel",
            reply_markup=admin_menu()
        )
        # ================= XABARLAR =================


@bot.message_handler(func=lambda message: True)
def messages(message):

    uid = message.from_user.id
    text = message.text


    add_user(message)


    if uid in blocked and uid != ADMIN_ID:

        bot.send_message(
            uid,
            "🚫 Siz bloklangansiz"
        )

        return



    # ================= ADMIN PANEL =================


    if uid == ADMIN_ID:


        # CHIQISH

        if text == "🚪 Chiqish":

            bot.send_message(
                uid,
                "Oddiy menyu",
                reply_markup=main_menu()
            )

            return



        # STATISTIKA

        if text == "📊 Statistika":

            cursor.execute(
                "SELECT COUNT(*),SUM(qr_count) FROM users"
            )

            data = cursor.fetchone()


            cursor.execute(
                "SELECT SUM(balance) FROM users"
            )

            money = cursor.fetchone()[0]


            bot.send_message(
                uid,
                f"""
📊 STATISTIKA

👥 Userlar:
{data[0]}

📱 Yaratilgan QR:
{data[1] or 0}

💰 Umumiy balans:
{money or 0} so'm
"""
            )

            return



        # PUL BERISH

        if text == "💰 Pul berish":

            user_mode[uid] = "give"

            bot.send_message(
                uid,
                """
ID va pul yuboring

Misol:
123456789 5000
"""
            )

            return



        if user_mode.get(uid) == "give":

            try:

                user_id, amount = text.split()

                user_id = int(user_id)
                amount = int(amount)


                user = get_user(user_id)


                if user:

                    cursor.execute(
                        """
                        UPDATE users
                        SET balance=balance+?
                        WHERE id=?
                        """,
                        (
                            amount,
                            user_id
                        )
                    )

                    db.commit()


                    bot.send_message(
                        uid,
                        "✅ Pul berildi"
                    )


                    bot.send_message(
                        user_id,
                        f"💰 Sizga {amount} so'm qo'shildi"
                    )


                else:

                    bot.send_message(
                        uid,
                        "❌ User topilmadi"
                    )


            except:

                bot.send_message(
                    uid,
                    "❌ Format xato"
                )


            user_mode.pop(uid)

            return




        # BONUS

        if text == "🎁 Bonus":

            user_mode[uid] = "bonus"

            bot.send_message(
                uid,
                "Bonus summasini yuboring:"
            )

            return



        if user_mode.get(uid) == "bonus":

            try:

                bonus = int(text)


                cursor.execute(
                    """
                    UPDATE users
                    SET balance=balance+?
                    """,
                    (bonus,)
                )


                db.commit()


                bot.send_message(
                    uid,
                    "🎁 Hamma userga bonus berildi"
                )


            except:

                bot.send_message(
                    uid,
                    "❌ Son yuboring"
                )


            user_mode.pop(uid)

            return



        # BLOKLASH

        if text == "🚫 Bloklash":

            user_mode[uid] = "block"

            bot.send_message(
                uid,
                "User ID yuboring:"
            )

            return



        if user_mode.get(uid) == "block":

            try:

                blocked.add(
                    int(text)
                )


                bot.send_message(
                    uid,
                    "🚫 Bloklandi"
                )

            except:

                pass


            user_mode.pop(uid)

            return




    # ================= HISOBIM =================


    if text == "💳 Hisobim":

        user = get_user(uid)


        bot.send_message(
            uid,
            f"""
💳 HISOBIM

💰 Balans:
{user[4]} so'm

📱 QR soni:
{user[6]}

💸 Ishlatilgan:
{user[5]} so'm
"""
        )

        return



    # ================= QR TANLASH =================


    if text == "🌐 Link":

        user_mode[uid] = "link"

        bot.send_message(
            uid,
            "🔗 Link yuboring:"
        )

        return



    if text == "📝 Matn":

        user_mode[uid] = "text"

        bot.send_message(
            uid,
            "📝 Matn yuboring:"
        )

        return



    if text == "📞 Telefon":

        user_mode[uid] = "phone"

        bot.send_message(
            uid,
            "📞 Raqam yuboring:"
        )

        return



    if text == "📧 Email":

        user_mode[uid] = "email"

        bot.send_message(
            uid,
            "📧 Email yuboring:"
        )

        return



    if text == "📶 Wi-Fi":

        user_mode[uid] = "wifi"

        bot.send_message(
            uid,
            "WiFi|Parol yuboring:"
        )

        return
        # ================= QR YARATISH =================


    if uid in user_mode:


        mode = user_mode[uid]


        data = text


        user = get_user(uid)


        # BALANS TEKSHIRISH

        if user[4] < QR_PRICE:

            bot.send_message(
                uid,
                f"""
❌ Balans yetarli emas

QR narxi:
{QR_PRICE} so'm

Sizda:
{user[4]} so'm
"""
            )

            user_mode.pop(uid)

            return



        if mode == "phone":

            data = "tel:" + text



        elif mode == "email":

            data = "mailto:" + text



        elif mode == "wifi":

            try:

                name,password = text.split("|")


                data = (
                    f"WIFI:T:WPA;"
                    f"S:{name};"
                    f"P:{password};;"
                )


            except:


                bot.send_message(
                    uid,
                    "❌ Format xato\nMisol: WiFi|12345678"
                )

                return




        # QR YASASH


        img = qrcode.make(data)


        img.save(
            "qr.png"
        )



        # PUL AYIRISH


        new_balance = user[4] - QR_PRICE

        new_spent = user[5] + QR_PRICE

        new_qr = user[6] + 1



        update_user(
            uid,
            new_balance,
            new_spent,
            new_qr
        )



        with open(
            "qr.png",
            "rb"
        ) as photo:


            bot.send_photo(
                uid,
                photo,
                caption=f"""
✅ QR kod tayyor

💸 {QR_PRICE} so'm yechildi

💰 Qolgan balans:
{new_balance} so'm
"""
            )



        user_mode.pop(uid)

        return





# ================= KONTAKT =================


@bot.message_handler(
    content_types=["contact"]
)
def contact(message):

    uid = message.from_user.id


    cursor.execute(
        """
        UPDATE users
        SET phone=?
        WHERE id=?
        """,
        (
            message.contact.phone_number,
            uid
        )
    )


    db.commit()


    bot.send_message(
        uid,
        "✅ Raqamingiz saqlandi",
        reply_markup=main_menu()
    )





# ================= RUN =================


print(
    "BOT ISHLADI"
)


bot.infinity_polling()
