from app.scrapers.rss.common import read_rss


def get_motorauthority_news():
    return read_rss(
        "https://www.motorauthority.com/rss",
        "MotorAuthority",
    )