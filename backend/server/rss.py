import feedparser  # type: ignore
import asyncio
import aiohttp
import os
from datetime import datetime, timezone
from typing import TypedDict, List
import logging
import time
from zoneinfo import ZoneInfo


class FeedEntry(TypedDict):
    title: str
    timestamp: datetime
    timestamp_human: str


def format_relative_time(dt: datetime) -> str:
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = now - dt

    seconds = int(diff.total_seconds())
    if seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    if seconds < 86400:
        hours = seconds // 3600
        return f"{hours}h"

    days = seconds // 86400
    return f"{days}d"


def parse_timestamp(entry, feed_url: str) -> datetime:
    timestamp = datetime(*entry.published_parsed[:6])
    if feed_url == "https://mothership.sg/feed/":
        # mothership.sg provides timestamps without any timezone info
        # but we know that the timestamps are in the Singapore timezone
        timestamp = timestamp.replace(tzinfo=ZoneInfo("Asia/Singapore"))

    elif timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return timestamp


async def parse_feed_url(feed_url: str) -> List[FeedEntry]:
    async with aiohttp.ClientSession() as session:
        logging.debug("parse_feed_url: %s", feed_url)
        async with session.get(feed_url) as response:
            content = await response.text()
            feed = feedparser.parse(content)
            items: List[FeedEntry] = [
                dict(
                    title=entry.title.strip(),
                    timestamp=parse_timestamp(entry, feed_url),
                    timestamp_human=format_relative_time(
                        parse_timestamp(entry, feed_url),
                    ),
                )
                for entry in feed.entries
            ]
            return items


async def parse_feeds_urls(feed_urls: list[str]) -> List[List[FeedEntry]]:
    tasks = [parse_feed_url(feed_url) for feed_url in feed_urls]
    return await asyncio.gather(*tasks)


async def parse_news_feeds_urls() -> List[FeedEntry]:
    feed_urls = os.environ.get("RSS_NEWS")
    if feed_urls and len(feed_urls) > 0:
        feeds = await parse_feeds_urls(feed_urls.split(","))
        results = sorted(
            [
                entry
                for feed in feeds
                for entry in feed
                if entry["timestamp"] and not entry["title"].startswith("ADV:")
            ],
            key=lambda x: x["timestamp"],
            reverse=True,
        )
        # for item in results:
        #     logging.debug(
        #         f"{item['title']}, {item['timestamp']}, {item['timestamp_human']}"
        #     )
        return results
    return []
