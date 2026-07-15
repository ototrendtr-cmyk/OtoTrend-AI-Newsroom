from app.database.source_crud import create_source

# ==========================================================
# OtoTrend AI CMS
# Source Seeder
# ==========================================================
#
# Bu dosya sistem ilk açıldığında
# eksik haber kaynaklarını otomatik olarak oluşturur.
#
# Aynı isimde kaynak varsa tekrar oluşturulmaz.
#
# ==========================================================

SOURCES = [

    # ======================================================
    # TÜRKİYE
    # ======================================================

    {
        "name": "Motor1 Türkiye",
        "website": "https://tr.motor1.com",
        "rss_url": "https://tr.motor1.com/rss/news/all/",
        "scraper": "Motor1TR",
        "language": "tr",
        "country": "Türkiye",
    },

    {
        "name": "LOG",
        "website": "https://www.log.com.tr",
        "rss_url": "",
        "scraper": "LOG",
        "language": "tr",
        "country": "Türkiye",
    },

    {
        "name": "DonanımHaber",
        "website": "https://www.donanimhaber.com",
        "rss_url": "",
        "scraper": "DonanimHaber",
        "language": "tr",
        "country": "Türkiye",
    },

    {
        "name": "Kolesa",
        "website": "https://kolesa.kz",
        "rss_url": "",
        "scraper": "Kolesa",
        "language": "ru",
        "country": "Kazakhstan",
    },

    # ======================================================
    # GLOBAL
    # ======================================================

    {
        "name": "Motor1",
        "website": "https://www.motor1.com",
        "rss_url": "https://www.motor1.com/rss/news/all/",
        "scraper": "Motor1",
        "language": "en",
        "country": "Global",
    },

    {
        "name": "Carscoops",
        "website": "https://www.carscoops.com",
        "rss_url": "https://www.carscoops.com/feed/",
        "scraper": "Carscoops",
        "language": "en",
        "country": "Global",
    },

    {
        "name": "AutoExpress",
        "website": "https://www.autoexpress.co.uk",
        "rss_url": "https://www.autoexpress.co.uk/rss.xml",
        "scraper": "AutoExpress",
        "language": "en",
        "country": "UK",
    },

    {
        "name": "Autoblog",
        "website": "https://www.autoblog.com",
        "rss_url": "https://www.autoblog.com/rss.xml",
        "scraper": "Autoblog",
        "language": "en",
        "country": "USA",
    },

    {
        "name": "InsideEVs",
        "website": "https://insideevs.com",
        "rss_url": "https://insideevs.com/rss/news/",
        "scraper": "InsideEVs",
        "language": "en",
        "country": "Global",
    },

    {
        "name": "Electrek",
        "website": "https://electrek.co",
        "rss_url": "https://electrek.co/feed/",
        "scraper": "Electrek",
        "language": "en",
        "country": "USA",
    },

    {
    "name": "Autocar",
    "website": "https://www.autocar.co.uk",
    "rss_url": "http://www.autocar.co.uk/rss",
    "scraper": "Autocar",
    "language": "en",
    "country": "UK",
    },
    {
    "name": "GreenCarReports",
    "website": "https://www.greencarreports.com",
    "rss_url": "https://www.greencarreports.com/rss",
    "scraper": "GreenCarReports",
    "language": "en",
    "country": "USA",
    },
    {
    "name": "Motor Authority",
    "website": "https://www.motorauthority.com",
    "rss_url": "https://www.motorauthority.com/rss",
    "scraper": "MotorAuthority",
    "language": "en",
    "country": "USA",
    },

    {
    "name": "CleanTechnica",
    "website": "https://cleantechnica.com",
    "rss_url": "https://cleantechnica.com/feed/",
    "scraper": "CleanTechnica",
    "language": "en",
    "country": "USA",
    },

    {
    "name": "Automotive News",
    "website": "https://www.autonews.com",
    "rss_url": "https://www.autonews.com/rss.xml",
    "scraper": "AutomotiveNews",
    "language": "en",
    "country": "USA",
    },

    {
    "name": "Autocar India",
    "website": "https://www.autocarindia.com",
    "rss_url": "https://www.autocarindia.com/rss",
    "scraper": "AutocarIndia",
    "language": "en",
    "country": "India",
    },

    {
    "name": "DriveSpark",
    "website": "https://www.drivespark.com",
    "rss_url": "https://www.drivespark.com/rss/",
    "scraper": "DriveSpark",
    "language": "en",
    "country": "India",
    },
    {
    "name": "Autoevolution",
    "website": "https://www.autoevolution.com",
    "rss_url": "https://www.autoevolution.com/rss/news.xml",
    "scraper": "Autoevolution",
    "language": "en",
    "country": "Global",
    },
    {
        "name": "CarBuzz",
        "website": "https://carbuzz.com",
        "rss_url": "",
        "scraper": "CarBuzz",
        "language": "en",
        "country": "USA",
    },
]

# ==========================================================
# Seeder
# ==========================================================

def seed_sources():
    """
    Sources tablosuna eksik kaynakları ekler.

    create_source() fonksiyonu aynı isimde kayıt varsa
    mevcut kaydı döndürdüğü için duplicate oluşmaz.
    """

    print("=" * 60)
    print("🌍 Source Seeder başladı...\n")

    processed = 0

    for source in SOURCES:

        create_source(
            name=source["name"],
            rss_url=source["rss_url"],
            website=source["website"],
            scraper=source["scraper"],
            language=source["language"],
            country=source["country"],
        )

        processed += 1

        print(
            f"✅ {source['name']:<20}"
            f" | {source['country']:<12}"
            f" | {source['scraper']}"
        )

    print("\n------------------------------------------------------------")
    print(f"📦 İşlenen kaynak sayısı : {processed}")
    print("✅ Source Seeder tamamlandı.")
    print("=" * 60)