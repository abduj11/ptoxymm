import os
import subprocess
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
# رابط الخدمة الخاص بك على Render
WEBHOOK_URL = f"https://<اسم-الخدمة-على-رندر>.onrender.com/{TOKEN}"

app_flask = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()

# دالة التحليل التي نستخدمها
async def analyze_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... (نفس دالة التحليل السابقة) ...
    pass

bot_app.add_handler(MessageHandler(filters.ATTACHMENT | filters.PHOTO, analyze_file))

# استقبال التحديثات من تليجرام
@app_flask.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put(update)
    return "OK", 200

@app_flask.route("/")
def home():
    return "Spider OSINT Bot is Online!"

if __name__ == "__main__":
    # تشغيل Flask فقط - لا تستخدم run_polling نهائياً
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)
