FROM python:3.10-slim

# تثبيت الأدوات الأساسية للتحليل
RUN apt-get update && apt-get install -y \
    libimage-exiftool-perl \
    binwalk \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# في Render، البوت لا يحتاج لفتح منفذ ويب إذا استخدمنا Polling
# لكننا سنبقي الكود مرناً
CMD ["python", "bot.py"]
