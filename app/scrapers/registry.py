from app.scrapers.rss.motor1 import get_motor1_news
from app.scrapers.rss.motor1_tr import get_motor1_tr_news
from app.scrapers.rss.carscoops import get_carscoops_news
from app.scrapers.rss.insideevs import get_insideevs_news
from app.scrapers.rss.electrek import get_electrek_news
from app.scrapers.rss.autoblog import get_autoblog_news
from app.scrapers.rss.autoexpress import get_autoexpress_news
from app.scrapers.rss.carbuzz import get_carbuzz_news
from app.scrapers.rss.autocar import get_autocar_news
from app.scrapers.html.log import get_log_news
from app.scrapers.html.donanimhaber import get_donanimhaber_news
from app.scrapers.html.kolesa import get_kolesa_news
from app.scrapers.rss.autoevolution import get_autoevolution_news
from app.scrapers.rss.greencarreports import get_greencarreports_news
from app.scrapers.rss.motorauthority import get_motorauthority_news
from app.scrapers.rss.cleantechnica import get_cleantechnica_news
from app.scrapers.rss.automotivenews import get_automotivenews_news
from app.scrapers.rss.autocarindia import get_autocarindia_news
from app.scrapers.rss.drivespark import get_drivespark_news

SCRAPER_REGISTRY = {

    # RSS
    "Autocar": get_autocar_news,
    "Motor1": get_motor1_news,
    "Motor1TR": get_motor1_tr_news,
    "Carscoops": get_carscoops_news,
    "InsideEVs": get_insideevs_news,
    "Electrek": get_electrek_news,
    "Autoblog": get_autoblog_news,
    "AutoExpress": get_autoexpress_news,
    "CarBuzz": get_carbuzz_news,
    "Autoevolution": get_autoevolution_news,
    "GreenCarReports": get_greencarreports_news,
    "MotorAuthority": get_motorauthority_news,
    "CleanTechnica": get_cleantechnica_news,
    "AutomotiveNews": get_automotivenews_news,
    "AutocarIndia": get_autocarindia_news,
    "DriveSpark": get_drivespark_news,

    # HTML
    "LOG": get_log_news,
    "DonanimHaber": get_donanimhaber_news,
    "Kolesa": get_kolesa_news,
}


def get_scraper_names():
    return sorted(SCRAPER_REGISTRY.keys())