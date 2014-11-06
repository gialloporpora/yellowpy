@echo off
set ifile=%1
set ofile=%~n1.7z
echo %ofile%

set tempfolder=%tmp%\rar27z
if exist %tempfolder% rd /s/q %tempfolder%
7z x %1 -o%tempfolder%
7z a "%ofile%" -t7z %tempfolder%\*
