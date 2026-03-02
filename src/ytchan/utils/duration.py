"""Parse ISO 8601 duration strings (e.g. PT1H2M3S) to seconds."""

import re


def parse_iso8601_duration(duration: str) -> int:
    """Return total seconds for an ISO 8601 duration string."""
    if not duration:
        return 0
    pattern = r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
    m = re.fullmatch(pattern, duration)
    if not m:
        return 0
    hours = int(m.group(1) or 0)
    minutes = int(m.group(2) or 0)
    seconds = int(m.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds
