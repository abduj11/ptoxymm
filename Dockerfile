# اختيار الصورة الأساسية
FROM python:3.10-slim

# تحديث النظام وتثبيت أدوات OSINT
RUN apt-get update && apt-get install -y \
    libimage-exiftool-perl \
    binwalk \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# إعداد دليل العمل
WORKDIR /app

# نسخ ملف المتطلبات أولاً
COPY requirements.txt .

# تثبيت المكتبات (هذا السطر هو الذي سيحل مشكلة ModuleNotFoundError)
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات الكود
COPY . .

# تشغيل البوت
CMD ["python", "bot.py"]
