import os

TOKEN = os.getenv("8370617478:AAHwWZRiyF72El1A_IOYpGXI2gicChcpe-c")
import telebot
import qrcode
from telebot import types

TOKEN = "8370617478:AAHwWZRiyF72El1A_IOYpGXI2gicChcpe-c"

ADMIN_ID = 7600986332

bot = telebot.TeleBot(TOKEN)


users = {}
blocked_users = set()
user_mode = {}

qr_count = 0
broadcast_mode = False



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
        "📱 Raqam yuborish"
    )

    return menu



def admin_menu():

    panel = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    panel.add(
        "📊 Statistika",
        "📢 Xabar yuborish"
    )

    panel.add(
        "🚫 Bloklash",
        "✅ Blokdan chiqarish"
    )

    panel.add(
        "🚪 Admin paneldan chiqish"
    )

    return panel



@bot.message_handler(commands=["start"])
def start(message):

    users[message.from_user.id] = {
        "username": message.from_user.username,
        "name": message.from_user.first_name
    }


    if message.from_user.id in blocked_users:

        bot.send_message(
            message.chat.id,
            "🚫 Siz bloklangansiz"
        )

        return



    if message.from_user.id == ADMIN_ID:

        bot.send_message(
            message.chat.id,
            "👑 Admin panel",
            reply_markup=admin_menu()
        )

    else:

        bot.send_message(
            message.chat.id,
            "🤖 QR Code bot",
            reply_markup=main_menu()
        )



@bot.message_handler(commands=["admin"])
def admin(message):

    if message.from_user.id == ADMIN_ID:

        bot.send_message(
            message.chat.id,
            "👑 Admin panel",
            reply_markup=admin_menu()
        )
        
@bot.message_handler(func=lambda message: True)
def messages(message):

    global qr_count
    global broadcast_mode


    uid = message.from_user.id
    text = message.text


    if uid in blocked_users and uid != ADMIN_ID:

        bot.send_message(
            uid,
            "🚫 Siz bloklangansiz"
        )

        return



    # ADMIN PANEL

    if uid == ADMIN_ID:


        if text == "🚪 Admin paneldan chiqish":

            bot.send_message(
                uid,
                "✅ Oddiy menyu",
                reply_markup=main_menu()
            )

            return



        if text == "📊 Statistika":

            info = "👥 Foydalanuvchilar:\n\n"

            for user_id,data in users.items():

                username = data["username"]

                if username:
                    username = "@" + username
                else:
                    username = "Username yo'q"


                info += (
                    f"🆔 {user_id}\n"
                    f"👤 {data['name']}\n"
                    f"🔗 {username}\n\n"
                )


            bot.send_message(
                uid,
                f"""
📊 STATISTIKA

👥 Userlar: {len(users)}
📱 QR soni: {qr_count}
🚫 Bloklangan: {len(blocked_users)}

{info}
"""
            )

            return



        if text == "🚫 Bloklash":

            user_mode[uid] = "block"

            bot.send_message(
                uid,
                "🚫 Blok qilinadigan ID yuboring:"
            )

            return



        if text == "✅ Blokdan chiqarish":

            user_mode[uid] = "unblock"

            bot.send_message(
                uid,
                "✅ Ochiladigan ID yuboring:"
            )

            return



        if text == "📢 Xabar yuborish":

            broadcast_mode = True

            bot.send_message(
                uid,
                "📢 Xabar matnini yuboring:"
            )

            return



        if broadcast_mode:

            broadcast_mode = False


            for user_id in users:

                try:

                    bot.send_message(
                        user_id,
                        "📢 Admin xabari:\n\n" + text
                    )

                except:

                    pass



            bot.send_message(
                uid,
                "✅ Xabar yuborildi"
            )

            return



        # BLOK / OCHISH

        if uid in user_mode:


            if user_mode[uid] == "block":

                try:

                    blocked_users.add(int(text))

                    bot.send_message(
                        uid,
                        "🚫 User bloklandi"
                    )

                except:

                    bot.send_message(
                        uid,
                        "❌ ID xato"
                    )


                user_mode.pop(uid)

                return



            if user_mode[uid] == "unblock":

                try:

                    blocked_users.discard(int(text))

                    bot.send_message(
                        uid,
                        "✅ User ochildi"
                    )

                except:

                    pass


                user_mode.pop(uid)

                return
            
    # QR MENYU

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
            "📞 Telefon raqam yuboring:"
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
            "📶 Format:\nWiFi nomi|Parol"
        )

        return



    # TELEFON KONTAKT

    if text == "📱 Raqam yuborish":

        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True
        )

        button = types.KeyboardButton(
            "📞 Kontakt yuborish",
            request_contact=True
        )

        keyboard.add(button)


        bot.send_message(
            uid,
            "Raqamingizni yuboring:",
            reply_markup=keyboard
        )

        return




    # QR YARATISH


    if uid in user_mode:


        mode = user_mode[uid]

        data = text



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




        img = qrcode.make(data)

        img.save("qr.png")


        qr_count += 1



        with open("qr.png","rb") as photo:


            bot.send_photo(
                uid,
                photo,
                caption="✅ QR kod tayyor!"
            )


        user_mode.pop(uid)




# KONTAKT QABUL QILISH

@bot.message_handler(content_types=["contact"])
def contact(message):

    users[message.from_user.id]["phone"] = (
        message.contact.phone_number
    )


    bot.send_message(
        message.chat.id,
        "✅ Raqam saqlandi"
    )




print("BOT ISHLADI")


bot.infinity_polling()
