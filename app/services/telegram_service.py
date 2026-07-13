import requests

from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(text):

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": False,
    }

    try:
        response = requests.post(url, data=data, timeout=15)

        if response.status_code == 200:
            print("📨 Telegram mesajı gönderildi.")
        else:
            print("❌ Telegram Hatası:", response.text)

    except Exception as e:
        print("❌ Telegram Exception:", e)