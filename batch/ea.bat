@echo off
if (%1)==() goto errore1
IF NOT EXIST %1 GOTO errore2
set filename=%~n1
set ext=%~x1
if %ext%==.flv set ext=.mp3
if %ext%==.mp4 set ext=.aac
ffmpeg -i %1 -acodec copy -vn %filename%%ext%
goto fine
:errore1
echo Non e' stato specificato nessun file in ingresso 
goto fine


:errore2
 echo Il file '%1' non esiste
 
 
 :fine
