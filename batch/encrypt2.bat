@echo off
set ext=.enk
if %~x1==%ext% goto decrypt
if %~x1==.gpg goto decrypt

:encrypt:
gpg -c -o  "%~1%ext%" %1
if %errorlevel%==0 del %1
goto end



:decrypt:
gpg -d -o "%~n1" %1
if %errorlevel%==0 del %1
goto end
:end:
