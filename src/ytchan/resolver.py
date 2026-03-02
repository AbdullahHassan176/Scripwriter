"""Resolve various channel inputs (URL, @handle, channelId, username) to a channel ID."""

import re
from dataclasses import dataclass
from functools import lru_cache
from urllib.parse import urlparse

from ytchan.api_client import YouTubeApiClient

_CHANNEL_ID_RE = re.compile(r"^UC[A-Za-z0-9_-]{22}$")


@dataclass
class ResolvedChannel:
    channel_id: str
    title: str


def _extract_from_url(url: str) -> tuple[str | None, str | None]:
    """Return (channel_id_or_none, handle_or_none) from a YouTube URL."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")

    # /channel/UCxxxx
    m = re.match(r"^/channel/(UC[A-Za-z0-9_-]{22})$", path)
    if m:
        return m.group(1), None

    # /@handle or /c/handle or /user/handle
    m = re.match(r"^/@(.+)$", path) or re.match(r"^/(?:c|user)/(.+)$", path)
    if m:
        return None, m.group(1)

    return None, None


@lru_cache(maxsize=64)
def resolve_channel(channel_input: str) -> ResolvedChannel:
    """Resolve any channel input to a ResolvedChannel."""
    client = YouTubeApiClient()
    channel_input = channel_input.strip()

    # Direct channel ID
    if _CHANNEL_ID_RE.match(channel_input):
        items = client.channels_list(channel_id=channel_input)
        if items:
            return ResolvedChannel(channel_id=items[0]["id"], title=items[0]["snippet"]["title"])
        raise ValueError(f"Channel not found: {channel_input}")

    # @handle (bare, no URL)
    if channel_input.startswith("@"):
        items = client.channels_list(handle=channel_input[1:])
        if items:
            return ResolvedChannel(channel_id=items[0]["id"], title=items[0]["snippet"]["title"])
        raise ValueError(f"Channel not found: {channel_input}")

    # URL
    if "youtube.com" in channel_input or "youtu.be" in channel_input:
        channel_id, handle = _extract_from_url(channel_input)
        if channel_id:
            items = client.channels_list(channel_id=channel_id)
        elif handle:
            items = client.channels_list(handle=handle)
        else:
            raise ValueError(f"Cannot parse YouTube URL: {channel_input}")
        if items:
            return ResolvedChannel(channel_id=items[0]["id"], title=items[0]["snippet"]["title"])
        raise ValueError(f"Channel not found for URL: {channel_input}")

    raise ValueError(f"Unrecognised channel input: {channel_input!r}")
