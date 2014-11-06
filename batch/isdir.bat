@echo off
set tempfile=temp.txt
set object=%~1
dir /b/ad "%object%" > %tempfile%
for /f %%i in (%tempfile%) do set foldername="%%i"
echo %foldername%