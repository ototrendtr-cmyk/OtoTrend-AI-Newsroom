from app.database.crud import save_news
from app.services.telegram_service import send_telegram_message
from app.scrapers.registry import SCRAPER_REGISTRY

from app.services.source_service import get_enabled_sources
from app.database.source_crud import (
    mark_source_run,
    mark_source_success,
    mark_source_error,
)



def update_news():

    print("=" * 60)
    print("🚗 Haber taraması başladı...\n")

    total_new = 0

    sources = get_enabled_sources()
    print(f"Toplam aktif kaynak: {len(sources)}")

    for s in sources:
        print(
        f"- {s.name} | scraper={s.scraper} | enabled={s.enabled}"
    )

    if not sources:

        print("⚠ Aktif kaynak bulunamadı.")
        print("=" * 60)
        return

    for source in sources:

        try:
            mark_source_run(source.name)

            scraper = SCRAPER_REGISTRY.get(source.scraper)

            if scraper is None:

                print(
                    f"⚠ Kaynak: {source.name} | "
                    f"Scraper: '{source.scraper}' registry'de bulunamadı."
                )

                continue

            news = scraper()

            new_news = save_news(news)
            mark_source_success(
                source.name,
                len(new_news),
            )

            if new_news:

                for item in new_news:

                    message = (
                        f"🚨 OtoTrend AI\n\n"
                        f"📰 {item.title}\n\n"
                        f"🔷 Kaynak: {item.source}\n\n"
                        f"🔗 {item.link}"
                    )

                    send_telegram_message(message)

            print(
                f"✅ {source.name:<25}"
                f"{len(new_news)} yeni haber"
            )

            total_new += len(new_news)

        except Exception as e:

            mark_source_error(
                source.name,
                str(e),
            )

            print(
                f"❌ Kaynak: {source.name} | "
                f"Hata: {str(e)}"
            )

    print("\n----------------------------------------")
    print(f"🆕 Toplam yeni haber: {total_new}")
    print("✔ Haber taraması tamamlandı")
    print("=" * 60)