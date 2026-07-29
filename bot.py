import telebot
import qrcode
import sqlite3

from telebot import types


# TOKEN SHU YERGA
TOKEN = "8370617478:AAHSzoSM401p7v0i6ioSI7R7laaok-Wn5L0"


bot = telebot.TeleBot(TOKEN)


ADMIN_ID = 7600986332
QR_PRICE = 150


# DATABASE

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

    if cursor.fetchone() is None:

        cursor.execute(
            """
            INSERT INTO users
            (id,username,name)
            VALUES(?,?,?)
            """,
            (
                uid,
                message.from_user.username,
                message.from_user.first_name
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



user_mode = {}
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

    return menu



def admin_menu():

    menu = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    menu.add(
        "📊 Statistika"
    )

    menu.add(
        "💰 Pul berish"
    )

    return menu



# ================= START =================


@bot.message_handler(commands=["start"])
def start(message):

    add_user(message)

    uid = message.from_user.id


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
🤖 QR BOT

💰 Boshlang'ich balans: 1000 so'm

QR narxi:
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
            "👑 Admin",
            reply_markup=admin_menu()
        )
        # ================= XABARLAR =================


@bot.message_handler(func=lambda message: True)
def messages(message):

    uid = message.from_user.id
    text = message.text

    add_user(message)


    # HISOB

    if text == "💳 Hisobim":

        user = get_user(uid)

        bot.send_message(
            uid,
            f"""
💳 HISOB

💰 Balans:
{user[3]} so'm

📱 QR:
{user[5]} ta

💸 Sarflangan:
{user[4]} so'm
"""
        )

        return



    # QR TANLASH


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
            "WiFi|Parol\nMisol:\nUyWifi|12345678"
        )

        return



    # QR YASASH


    if uid in user_mode:

        user = get_user(uid)


        if user[3] < QR_PRICE:

            bot.send_message(
                uid,
                "❌ Balans yetarli emas"
            )

            user_mode.pop(uid)

            return



        data = text

        mode = user_mode[uid]


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
                    "❌ Format xato"
                )

                return



        qr = qrcode.make(data)

        qr.save("qr.png")



        update_user(
            uid,
            user[3]-QR_PRICE,
            user[4]+QR_PRICE,
            user[5]+1
        )


        with open(
            "qr.png",
            "rb"
        ) as photo:


            bot.send_photo(
                uid,
                photo,
                caption="✅ QR kod tayyor"
            )


        user_mode.pop(uid)

        return
    # ================= ADMIN STAT =================


@bot.message_handler(commands=["stat"])
def stat(message):

    if message.from_user.id == ADMIN_ID:

        cursor.execute(
            "SELECT COUNT(*) FROM users"
        )

        users = cursor.fetchone()[0]


        bot.send_message(
            message.chat.id,
            f"""
📊 STATISTIKA

👥 Userlar:
{users}
"""
        )



# ================= KONTAKT =================


@bot.message_handler(
    content_types=["contact"]
)
def contact(message):

    bot.send_message(
        message.chat.id,
        "✅ Raqam saqlandi",
        reply_markup=main_menu()
    )



# ================= RUN =================


print("BOT ISHLADI")


bot.infinity_polling()
