import os
import telebot
from telebot import types
from pymongo import MongoClient

# सेटिंग्स
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_ID = 7162565886 
CHANNEL_ID = "@HackersColony"
YOUTUBE_URL = "https://youtube.com/@HackersColonyTech"
WEB_URL = os.getenv("WEB_URL")

bot = telebot.TeleBot(BOT_TOKEN)
client = MongoClient(MONGO_URI)
db = client['RoshanTrackerDB']
users_col = db['users']

def is_joined(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({"user_id": user_id})

    markup = types.InlineKeyboardMarkup()
    if not is_joined(user_id):
        markup.add(types.InlineKeyboardButton("📢 Join Telegram", url=f"https://t.me/{CHANNEL_ID[1:]}"))
        markup.add(types.InlineKeyboardButton("📺 Subscribe YouTube", url=YOUTUBE_URL))
        markup.add(types.InlineKeyboardButton("✅ Verify Joining", callback_data="check"))
        bot.send_message(user_id, "🛡️ **Welcome!**\n\nPlease join our channels to unlock premium tracking tools.", reply_markup=markup, parse_mode="Markdown")
    else:
        show_menu(user_id)

def show_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📍 Create Tracking Link", callback_data="gen_link"),
        types.InlineKeyboardButton("📊 My Stats", callback_data="stats"),
        types.InlineKeyboardButton("📞 Contact Support (Admin)", url="https://t.me/Roshanali000")
    )
    bot.send_message(chat_id, "💎 **Dashboard Active**\nSelect a service:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id == ADMIN_ID:
        text = message.text.replace('/broadcast ', '')
        if text == '/broadcast': return
        users = users_col.find()
        for u in users:
            try: bot.send_message(u['user_id'], text)
            except: pass
        bot.send_message(ADMIN_ID, "✅ Broadcast Complete!")

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == "check":
        if is_joined(call.message.chat.id): show_menu(call.message.chat.id)
        else: bot.answer_callback_query(call.id, "⚠️ Join first!", show_alert=True)
    elif call.data == "gen_link":
        link = f"{WEB_URL}/?id={call.message.chat.id}"
        bot.send_message(call.message.chat.id, f"🚀 **Your Link:**\n`{link}`", parse_mode="Markdown")

bot.polling()
  
