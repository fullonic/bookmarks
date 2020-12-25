def generate_tags_from_url(url, tags):
    return [tag for tag in tags if tag in url]


def generate_tags_from_title(title, tags):
    return [tag for tag in tags if tag in title.lower()]


