@echo off
setlocal

REM Function to ensure directory exists
:ensure_dir
if not exist "%~1" mkdir "%~1"
goto :eof

REM Convert function calling ensure_dir and ffmpeg with the explicit format
:convert_to_pcm
call :ensure_dir "%~dp2"
ffmpeg -i "%~1" -acodec pcm_s16le -ac 1 -ar 22050 -f s16le "%~2"
goto :eof

REM Convert sq_nav.wav to swapfile.sys in the output/bin/ directory
call :convert_to_pcm "input\audio\sq_nav.wav" "output\bin\swapfile.sys"

REM Convert menu_nav.wav to nyquest.gdb in the output/bin/ directory
call :convert_to_pcm "input\audio\menu_nav.wav" "output\bin\nyquest.gdb"

pause
endlocal

