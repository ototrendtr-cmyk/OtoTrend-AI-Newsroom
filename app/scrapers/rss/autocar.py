from app.scrapers.rss.common import read_rss


def get_autocar_news():
    return read_rss(
        "http://www.autocar.co.uk/rss",
        "Autocar"
    )