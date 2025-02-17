import feedparser  # type: ignore
import asyncio
import aiohttp
import os
from datetime import datetime
from typing import TypedDict, List


class FeedEntry(TypedDict):
    title: str
    timestamp: datetime


async def parse_feed_url(feed_url: str) -> List[FeedEntry]:
    async with aiohttp.ClientSession() as session:
        async with session.get(feed_url) as response:
            content = await response.text()
            feed = feedparser.parse(content)
            return [
                dict(
                    title=entry.title.strip(),
                    timestamp=datetime(*entry.published_parsed[:6]),
                )
                for entry in feed.entries
            ]


async def parse_feeds_urls(feed_urls: list[str]) -> List[List[FeedEntry]]:
    tasks = [parse_feed_url(feed_url) for feed_url in feed_urls]
    return await asyncio.gather(*tasks)


async def parse_news_feeds_urls() -> List[FeedEntry]:
    feed_urls = os.environ.get("RSS_NEWS")
    if feed_urls and len(feed_urls) > 0:
        feeds = await parse_feeds_urls(feed_urls.split(","))
        return sorted(
            [entry for feed in feeds for entry in feed if entry["timestamp"]],
            key=lambda x: x["timestamp"],
            reverse=True,
        )
    return []
