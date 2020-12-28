def generate_tags(url, title, tags):
    from_title = generate_tags_from_title(title, tags)
    from_url = generate_tags_from_url(url, tags)
    return set(from_title + from_url)


def generate_tags_from_url(url, tags):
    return [tag for tag in tags if tag in url]


def generate_tags_from_title(title, tags):
    return [tag for tag in tags if tag in title.lower()]
