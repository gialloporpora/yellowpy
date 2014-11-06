@echo off
set tempfile="%~dp0\temp.txt"
set mimetypes=%~dp0mimetypes.txt
REM Extracting the extension of the file
set ext=%~x1_
REM Removing the period for using as correct variable name
set ext=%ext:~1,-1%
REM Load mimetypes from file, if some mimetype is missing update the file mimetypes.txt
REM for any mimetypes is created a variable mime_mimetype, for example mime_png for image/png
for /f "delims== tokens=1,2 eol=#" %%i  in (%mimetypes%) do set mime_%%i=%%j
if not defined mime_%ext%% goto mimeundefined
call set contenttype=%%mime_%ext%%%
openssl enc -e -a -in %1 -out %tempfile%
if "%2"=="one" (sed -n "H;${x;s/\n//g;s/.*/data:%contenttype%;base64,&/;p}" %tempfile% > base64.txt) else (sed -e "1{s/.*/data:%contenttype%;base64,&/;}"  %tempfile% > base64.txt)
echo Ok, your base64 encoded file is in base64.txt, open it and good luck my friend!
echo.
goto end
:mimeundefined
echo An error occured, mimetype for this file is not defined
echo I am sorry for this inconvenience
echo edit the mimetypes.txt file and add the mimetype for this file's extension (search it with google, your best friend for these kind of issues)
echo.
goto end


:end: