@echo off
REM Found here: http://stackoverflow.com/questions/4002819/finding-the-path-of-the-program-that-will-execute-from-the-command-line-in-windo
rem - search for the given file in the directories specified by the path, and display the first match
rem
rem    The main ideas for this script were taken from Raymond Chen's blog:
rem
rem         http://blogs.msdn.com/b/oldnewthing/archive/2005/01/20/357225.asp
rem
rem
rem - it'll be nice to at some point extend this so it won't stop on the first match. That'll
rem     help diagnose situations with a conflict of some sort.
rem

setlocal

rem - search the current directory as well as those in the path
set PATHLIST=.;%PATH%
set EXTLIST=%PATHEXT%

if not "%EXTLIST%" == "" goto :extlist_ok
set EXTLIST=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH
:extlist_ok

rem - first look for the file as given (not adding extensions)
for %%i in (%1) do if NOT "%%~$PATHLIST:i"=="" echo %%~$PATHLIST:i

rem - now look for the file adding extensions from the EXTLIST
for %%e in (%EXTLIST%) do @for %%i in (%1%%e) do if NOT "%%~$PATHLIST:i"=="" echo %%~$PATHLIST:i

