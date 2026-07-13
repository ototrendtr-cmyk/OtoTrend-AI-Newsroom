from app.scrapers.sources import SOURCES
from app.database.crud import save_news
from app.services.telegram_service import send_telegram_message


def update_news():

    print("=" * 60)
    print("🚗 Haber taraması başladı...\n")

    total_new = 0

    for source in SOURCES:

        try:
            news = source()

            new_news = save_news(news)

            # Yeni haber varsa Telegram'a gönder
            if new_news:

                for item in new_news:

                    message = (
                        f"🚨 OtoTrend AI\n\n"
                        f"📰 {item['title']}\n\n"
                        f"🏷 Kaynak: {item['source']}\n\n"
                        f"🔗 {item['link']}"
                    )

                    send_telegram_message(message)

            print(
                f"✅ {source.__name__:<25} "
                f"{len(new_news)} yeni haber"
            )

            total_new += len(new_news)

        except Exception as e:

            print(f"❌ {source.__name__}: {e}")

    print("\n----------------------------------------")
    print(f"🆕 Toplam yeni haber: {total_new}")
    print("✔ Haber taraması tamamlandı")
    print("=" * 60)