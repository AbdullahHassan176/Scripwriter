ytchan - YouTube Channel Data: Cleo Abram
Channel ID: UC415bOPUcGSamy543abLmRA

FOLDER STRUCTURE
================
videos_metadata_raw.json  - Raw video metadata from YouTube API (all videos)
videos_ranked.csv         - Videos ranked by popularity (spreadsheet)
videos_ranked.jsonl       - Videos ranked by popularity (one JSON per line)
transcripts_index.csv     - Transcript fetch status per video
dataset.jsonl             - Combined metadata + transcript text for analysis
channel_info.json         - Channel ID and title (manifest)
transcripts/              - Per-video transcript files
  <videoId>.json          - Raw transcript segments (timestamps)
  <videoId>.txt           - Plain text transcript

NOTE ON TRANSCRIPTS (popularity order)
--------------------------------------
Transcripts are fetched in popularity order (rank 1 = most viewed). With a request
limit, the first N transcripts you get are the channel's top N videos by views.
- transcripts_index.csv has popularity_rank (1-based) and has_transcript (yes/no).
- dataset.jsonl is built in the same order: line 1 = top video; each row has
  popularity_rank and has_transcript so you can filter or slice easily.
Use `ytchan import-transcripts <folder>` to import tactiq-downloaded transcripts.
