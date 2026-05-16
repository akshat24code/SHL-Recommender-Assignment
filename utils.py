def validate_url(url: str, catalog: list[dict]) -> bool:
    return any(item["url"] == url for item in catalog)


def deduplicate_by_url(items: list[dict]) -> list[dict]:

    seen = set()

    unique = []

    for item in items:

        if item["url"] not in seen:

            unique.append(item)

            seen.add(item["url"])

    return unique