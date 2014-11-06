@echo off
REM Set you API KEY http://imgur.com/register/api_anon
set apikey=4f3b464882b5d95a4a2deaad44977c3f

REM Usage:
REM img file_path [title] [caption]
REM img url [title] [caption]
REM title and caption are optional, quote them if they contains spaces or strange characters

REM Set the path where are located curl.exe and sed.exe
REM is you use Cygwin, install the curl's package (sed is included by default in standard installation) and uncomment this line http://imgur.com/CioIf
REM PATH=%PATH%;C:\cygwin\bin


REM Removing quotes from parameters to avoid problems with curl
set image=%~1
set prefix=%image:~0,4%
set title=%~2
set caption=%~3


set historyfile="%~dp0imgur_history.txt"

echo     imgur uploader via CURL version 1.0 by @gialloporpora
echo.
if "%image%"=="" goto help
if  /i %1==help goto help
if  /i %1==-h goto help
if  /i %1==view goto showhistory
if  /i %1==-v goto showhistory

REM /i case insensitive match
if /i  %prefix%==http goto urlupload
:fileupload:
if not exist %1 goto filenotfound
curl -F "title=%title%" -F "caption=%caption%"   -F "image=@%image%" -F "key=%apikey%" http://api.imgur.com/2/upload.xml > curl.html
goto success

:filenotfound:
echo File not found
goto end


:urlupload:
curl -d "image=%image%" -d "title=%title%" -d "caption=%caption%" -d "key=%apikey%"  http://api.imgur.com/2/upload.xml > curl.html

:success:
sed -n -e "/<original>/{s/.*<original>\(.*\)<\/original><imgur_page>\(.*\)<\/imgur_page><delete_page>\(.*\)<\/delete_page>.*<large_thumbnail>\(.*\)<\/large_thumbnail>.*/Original image:\t\1\nImage page:\t\2\nThumbnail:\t\4\nDeletion Page:\t\3\n/;p}"  curl.html > temp.txt
type temp.txt
date /T >> %historyfile%
time /T >> %historyfile%
echo Title: %title% >> %historyfile%
echo Caption: %caption% >> %historyfile%
type temp.txt >> %historyfile%
del temp.txt
del curl.html
goto end

:help:
echo Usage:
echo.
echo 	img filename [title] [caption]
echo 	img url [title] [caption]
echo.
echo title and caption are optional, if you use spaces inside them remember to quote them
echo.
echo * Type `img help' to show this help
echo * Type `img view' to show all your uploaded images
goto end

:showhistory:
type %historyfile%




:end: