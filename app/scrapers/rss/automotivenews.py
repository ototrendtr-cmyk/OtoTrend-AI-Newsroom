from app.scrapers.rss.common import read_rss


def get_automotivenews_news():
    return read_rss(
        "https://www.autonews.com/rss.xml",
        "AutomotiveNews",
    )