from app.scrapers.rss.common import read_rss

def get_autoexpress_news():
    return read_rss(
        "https://www.autoexpress.co.uk/rss.xml",
        "AutoExpress"
    )