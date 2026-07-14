from app.scrapers.rss.motor1 import get_motor1_news
from app.scrapers.rss.carscoops import get_carscoops_news
from app.scrapers.rss.autoexpress import get_autoexpress_news

SCRAPER_REGISTRY = {
    "Motor1": get_motor1_news,
    "Carscoops": get_carscoops_news,
    "AutoExpress": get_autoexpress_news,
}