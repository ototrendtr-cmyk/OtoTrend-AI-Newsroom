def validate(source):

    errors = []

    if source.scraper == "RSS" and not source.rss_url:
        errors.append("RSS URL boş")

    if not source.website:
        errors.append("Website eksik")

    return errors