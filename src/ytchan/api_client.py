"""Thin wrapper around the YouTube Data API v3."""

import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ytchan.config import get_settings

logger = logging.getLogger(__name__)

_PAGE_SIZE = 50


def _build_service():
    settings = get_settings()
    return build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY, cache_discovery=False)


class YouTubeApiClient:
    def __init__(self):
        self._svc = _build_service()

    @retry(
        retry=retry_if_exception_type(HttpError),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def channels_list(self, *, channel_id: str | None = None, handle: str | None = None) -> list[dict]:
        kwargs: dict = {"part": "snippet,contentDetails", "maxResults": 1}
        if channel_id:
            kwargs["id"] = channel_id
        elif handle:
            kwargs["forHandle"] = handle
        resp = self._svc.channels().list(**kwargs).execute()
        return resp.get("items", [])

    @retry(
        retry=retry_if_exception_type(HttpError),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def playlist_items_list(self, playlist_id: str, page_token: str | None = None) -> dict:
        kwargs = {"part": "contentDetails", "playlistId": playlist_id, "maxResults": _PAGE_SIZE}
        if page_token:
            kwargs["pageToken"] = page_token
        return self._svc.playlistItems().list(**kwargs).execute()

    @retry(
        retry=retry_if_exception_type(HttpError),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def videos_list(self, video_ids: list[str]) -> list[dict]:
        items: list[dict] = []
        for i in range(0, len(video_ids), _PAGE_SIZE):
            chunk = video_ids[i : i + _PAGE_SIZE]
            resp = (
                self._svc.videos()
                .list(
                    part="snippet,statistics,contentDetails",
                    id=",".join(chunk),
                    maxResults=_PAGE_SIZE,
                )
                .execute()
            )
            items.extend(resp.get("items", []))
        return items
