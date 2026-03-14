import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def analyze_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # استقبال الملف
    file = await update.message.effective_attachment.get_file()
    file_path = f"downloads/{file.file_id}"
    os.makedirs("downloads", exist_ok=True)
    await file.download_to_drive(file_path)

    await update.message.reply_text("🔎 جاري فحص الملف بأدوات OSINT...")

    # 1. تحليل Metadata (ExifTool)
    exif = subprocess.getoutput(f"exiftool {file_path}")
    
    # 2. فحص الملفات المخفية (Binwalk)
    binwalk = subprocess.getoutput(f"binwalk {file_path}")

    report = f"📊 **نتائج التحليل:**\n\n**ExifTool:**\n`{exif[:500]}`...\n\n**Binwalk:**\n`{binwalk[:500]}`"
    await update.message.reply_text(report, parse_mode="Markdown")
    
    # تنظيف الملفات بعد التحليل
    os.remove(file_path)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    # معالج لاستقبال الصور والملفات
    app.add_handler(MessageHandler(filters.ATTACHMENT | filters.PHOTO, analyze_file))
    
    print("🚀 Spider OSINT Bot is running on Render...")
    app.run_polling()
