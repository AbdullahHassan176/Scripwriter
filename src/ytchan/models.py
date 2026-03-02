"""Pydantic models for YouTube video data."""

from pydantic import BaseModel, Field


def _int(v) -> int:
    try:
        return int(v or 0)
    except (TypeError, ValueError):
        return 0


class VideoMeta(BaseModel):
    videoId: str
    title: str = ""
    publishedAt: str = ""
    duration: int = 0
    viewCount: int = Field(0, alias="viewCount")
    likeCount: int = Field(0, alias="likeCount")
    commentCount: int = Field(0, alias="commentCount")
    tags: list[str] = []
    description: str = ""
    thumbnailUrl: str = ""

    model_config = {"populate_by_name": True}


def video_from_api_item(item: dict) -> dict:
    """Convert a YouTube API videos.list item to a flat dict."""
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    content = item.get("contentDetails", {})
    thumbnails = snippet.get("thumbnails", {})
    thumb = (
        thumbnails.get("maxres")
        or thumbnails.get("high")
        or thumbnails.get("medium")
        or thumbnails.get("default")
        or {}
    )
    from ytchan.utils.duration import parse_iso8601_duration

    return {
        "videoId": item.get("id", ""),
        "title": snippet.get("title", ""),
        "publishedAt": snippet.get("publishedAt", ""),
        "duration": parse_iso8601_duration(content.get("duration", "")),
        "viewCount": _int(stats.get("viewCount")),
        "likeCount": _int(stats.get("likeCount")),
        "commentCount": _int(stats.get("commentCount")),
        "tags": snippet.get("tags") or [],
        "description": snippet.get("description", ""),
        "thumbnailUrl": thumb.get("url", ""),
    }
