@echo off
;; This batch file convert a DVD into an AVI file
;; You need ffmpeg and mencoder
;; ffmpeg: http://ffmpeg.zeranoe.com/builds/win32/static/
;; mencoder: http://oss.netfarm.it/mplayer-win32.php
;; Set the correct path of mencoder.exe and ffmpeg.exe in the following line
path="%programfiles%\ffmpeg";"%programfiles%\mplayer"
echo %path%