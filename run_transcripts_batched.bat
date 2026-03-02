@echo off
setlocal
set PYTHONIOENCODING=utf-8

REM Max videos to process per channel this round. Already-fetched are skipped.
REM Keep "new" requests under ~25 per channel per run to avoid IP block.
REM First run: 25. Then 50, 75, 100, ... (increase by 25 each round).
set MAX=25
if not "%~1"=="" set MAX=%~1

echo ========================================
echo ytchan - Transcripts (batched, max %MAX% per channel)
echo Use proxy: set YTCHAN_PROXY or HTTPS_PROXY before running
echo ========================================

call python -m ytchan fetch-transcripts "https://www.youtube.com/@thomasmulligan" --max %MAX%
call python -m ytchan build-dataset "https://www.youtube.com/@thomasmulligan"

call python -m ytchan fetch-transcripts "https://www.youtube.com/@kallawaytech" --max %MAX%
call python -m ytchan build-dataset "https://www.youtube.com/@kallawaytech"

call python -m ytchan fetch-transcripts "https://www.youtube.com/@H1T1" --max %MAX%
call python -m ytchan build-dataset "https://www.youtube.com/@H1T1"

call python -m ytchan fetch-transcripts "https://www.youtube.com/@CleoAbram" --max %MAX%
call python -m ytchan build-dataset "https://www.youtube.com/@CleoAbram"

call python -m ytchan fetch-transcripts "https://www.youtube.com/@RealLifeLore" --max %MAX%
call python -m ytchan build-dataset "https://www.youtube.com/@RealLifeLore"

call python -m ytchan fetch-transcripts "https://www.youtube.com/@youshaei" --max %MAX%
call python -m ytchan build-dataset "https://www.youtube.com/@youshaei"

call python -m ytchan fetch-transcripts "https://www.youtube.com/@MrBeast" --max %MAX%
call python -m ytchan build-dataset "https://www.youtube.com/@MrBeast"

echo ========================================
echo Round done. To fetch more, run again with higher max:
echo   run_transcripts_batched.bat 50
echo   run_transcripts_batched.bat 75
echo   ... (increase by 25 each round; wait 30-60 min between rounds if no proxy)
echo ========================================
goto :eof
