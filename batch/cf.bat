@echo off
set param=%~1
if "%param%"=="" goto notfound
if exist "%param%" (goto ok) else (goto notfound)
:ok:
set isfolder=%~a1
if  /i "%isfolder:~0,1%"=="d" (goto execute) else (goto notfolder)
:execute:
set name=%~n1
md "%name%"
xcopy /i /e "%param%" "%name%"
goto end
:notfolder:
echo Sorry, this is not a folder
goto end

:notfound:
echo Sorry, you have passed an invalid parameter


:end: