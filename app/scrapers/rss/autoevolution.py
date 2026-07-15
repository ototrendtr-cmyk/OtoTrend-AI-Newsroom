from app.scrapers.rss.common import read_rss


def get_autoevolution_news():
    return read_rss(
        "https://www.autoevolution.com/rss.xml",
        "Autoevolution",
    )