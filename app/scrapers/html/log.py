from app.scrapers.html.common import read_html


def get_log_news():

    return read_html(
        url="https://www.log.com.tr/asfalt/",
        source_name="LOG",
        article_selector="article",
        title_selector="h2 a, h3 a"
    )