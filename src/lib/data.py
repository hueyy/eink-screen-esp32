from micropython import const


def strip_html(input: str):
    import re

    return re.sub("<[^<]+?>", "", input)


def get_latest_toot_by_tag(tag: str) -> tuple[str, str, str, str] | None:
    import urequests

    response = urequests.get(
        url=f"https://kopiti.am/api/v1/timelines/tag/{tag}?limit=1"
    )
    if response.status_code == const(200):
        try:
            toot_content = strip_html(response.json()[0]["content"])
            toot_author_name = response.json()[0]["account"]["display_name"]
            toot_author_username = response.json()[0]["account"]["username"]
            toot_timestamp = response.json()[0]["account"]["created_at"]
            return (
                toot_author_name,
                toot_author_username,
                toot_content,
                toot_timestamp,
            )

        except IndexError:
            return None
    else:
        return None
