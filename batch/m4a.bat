@echo off
REM REM Download mp4box from here: http://www.hydrogenaudio.org/forums/index.php?showtopic=81679&st=0&p=710344&#entry710344
REM Direct link to mp4box: http://download2.videohelp.com/download/MP4Box-0.4.6-rev2080.zip (Windows)
REM Download ffmpeg from here: http://sourceforge.net/projects/mplayer-win32/files/FFmpeg/
if (%1)==() goto errore1
IF NOT EXIST %1 GOTO errore2
set filename=%~n1
ffmpeg -i %1 -acodec copy -vn temp.aac
mp4box -add temp.aac %filename%.m4a
REM del temp.aac
del %1
goto fine
:errore1
echo Non e' stato specificato nessun file in ingresso 
goto fine


:errore2
 echo Il file '%1' non esiste
 
 
 :fine
