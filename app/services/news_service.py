from app.database.crud import save_news

from app.scrapers.registry import (
    get_scraper_function,
    get_scraper_type,
)

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
            f"- {s.name}"
            f" | scraper={s.scraper}"
            f" | enabled={s.enabled}"
        )

    if not sources:

        print("⚠ Aktif kaynak bulunamadı.")
        print("=" * 60)
        return

    for source in sources:

        try:

            mark_source_run(source.name)

            scraper = get_scraper_function(source.scraper)

            if scraper is None:

                print(
                    f"⚠ Kaynak: {source.name}"
                    f" | Scraper: '{source.scraper}' bulunamadı."
                )

                continue

            scraper_type = get_scraper_type(source.scraper)

            print(
                f"▶ {source.name}"
                f" [{scraper_type}]"
            )

            # Generic RSS
            if source.scraper == "RSS":

                news = scraper(
                    url=source.rss_url,
                    source_name=source.name,
                )

            else:

                news = scraper()

            new_news = save_news(news)

            mark_source_success(
                source.name,
                len(new_news),
            )

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
                f"❌ Kaynak: {source.name}"
                f" | {str(e)}"
            )

    print("\n----------------------------------------")
    print(f"🆕 Toplam yeni haber: {total_new}")
    print("✔ Haber taraması tamamlandı")
    print("=" * 60)