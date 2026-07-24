import telebot
import qrcode
from telebot import types

TOKEN = "7901916599:AAE0AuvV7zQb3r6CTX8MXLiiP6eTKTLBBns"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🌐 Link")
    btn2 = types.KeyboardButton("📞 Telefon")
    btn3 = types.KeyboardButton("📍 Joylashuv")
    btn4 = types.KeyboardButton("📶 WiFi")
    btn5 = types.KeyboardButton("📝 Matn")

    keyboard.add(btn1, btn2)
    keyboard.add(btn3, btn4)
    keyboard.add(btn5)

    bot.send_message(
        message.chat.id,
        "QR turini tanlang 👇",
        reply_markup=keyboard
    )


user_type = {}


@bot.message_handler(content_types=["text"])
def message(message):

    chat = message.chat.id

    if message.text == "🌐 Link":
        user_type[chat] = "link"
        bot.send_message(chat, "Link yuboring:")

    elif message.text == "📞 Telefon":
        user_type[chat] = "phone"
        bot.send_message(chat, "Telefon raqam yuboring:")

    elif message.text == "📍 Joylashuv":
        user_type[chat] = "geo"
        bot.send_message(chat, "Lokatsiya yuboring:\nMisol: 41.311081,69.240562")

    elif message.text == "📶 WiFi":
        user_type[chat] = "wifi"
        bot.send_message(chat, "WiFi nomi va parolini yuboring:\nMisol: Wifi;12345678")

    elif message.text == "📝 Matn":
        user_type[chat] = "text"
        bot.send_message(chat, "Matn yuboring:")

    else:
        create_qr(message)


def create_qr(message):

    chat = message.chat.id
    text = message.text

    if user_type.get(chat) == "phone":
        text = "tel:" + text

    elif user_type.get(chat) == "geo":
        text = "geo:" + text

    elif user_type.get(chat) == "wifi":
        data = text.split(";")
        text = f"WIFI:T:WPA;S:{data[0]};P:{data[1]};;"

    qr = qrcode.make(text)
    qr.save("qr.png")

    with open("qr.png", "rb") as photo:
        bot.send_photo(
            chat,
            photo,
            caption="✅ QR kod tayyor"
        )


bot.infinity_polling()