@echo off
setlocal
set PYTHONIOENCODING=utf-8

REM Automated transcript loop: fetches up to N per channel per round via yt-dlp,
REM waits W minutes, then retries. Already-fetched are skipped.
REM Stops automatically when no new transcripts are found in a round.
REM Press Ctrl+C to stop early.
set MAX=25
set WAIT=5
if not "%~1"=="" set MAX=%~1
if not "%~2"=="" set WAIT=%~2

echo ========================================
echo ytchan - Transcript loop (max %MAX%/channel/round, wait %WAIT% min)
echo ========================================

python -m ytchan fetch-transcripts-loop ^
  "https://www.youtube.com/@thomasmulligan" ^
  "https://www.youtube.com/@kallawaytech" ^
  "https://www.youtube.com/@H1T1" ^
  "https://www.youtube.com/@CleoAbram" ^
  "https://www.youtube.com/@RealLifeLore" ^
  "https://www.youtube.com/@youshaei" ^
  "https://www.youtube.com/@MrBeast" ^
  --max-per-round %MAX% --wait-minutes %WAIT%

echo ========================================
echo Loop finished.
echo ========================================
