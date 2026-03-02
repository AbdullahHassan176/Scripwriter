@echo off
setlocal
set PYTHONIOENCODING=utf-8

REM Fetch metadata only (videos + rank + empty dataset) for all 7 channels.
REM This is fast — YouTube API only, no transcript fetching.
REM After this, run run_transcripts_loop.bat to fetch transcripts automatically.

echo ========================================
echo ytchan - Fetch metadata for 7 channels
echo ========================================

call python -m ytchan fetch-metadata "https://www.youtube.com/@thomasmulligan"
if errorlevel 1 goto :error

call python -m ytchan fetch-metadata "https://www.youtube.com/@kallawaytech"
if errorlevel 1 goto :error

call python -m ytchan fetch-metadata "https://www.youtube.com/@H1T1"
if errorlevel 1 goto :error

call python -m ytchan fetch-metadata "https://www.youtube.com/@CleoAbram"
if errorlevel 1 goto :error

call python -m ytchan fetch-metadata "https://www.youtube.com/@RealLifeLore"
if errorlevel 1 goto :error

call python -m ytchan fetch-metadata "https://www.youtube.com/@youshaei"
if errorlevel 1 goto :error

call python -m ytchan fetch-metadata "https://www.youtube.com/@MrBeast"
if errorlevel 1 goto :error

echo ========================================
echo Metadata done! Now run: run_transcripts_loop.bat
echo ========================================
goto :eof

:error
echo Pipeline failed. Check logs\
exit /b 1
