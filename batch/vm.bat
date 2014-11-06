@echo off
set tempfile=temp.txt
set cmd=%~1
if  /I "%cmd%"=="init" goto init
REM Reading settings from configuration file 
if not exist .verbatim goto notvmdir
FOR /F "delims=== tokens=1,2" %%i in (.verbatim) do set %%i=%%j
echo %files% > %tempfile%
sed "s/,/\n/g" %tempfile% -i
if /I "%cmd%"=="info" goto info
if /I "%cmd%"=="up" goto backup

:info

:backup
set backupdate=%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%
if not exist backup md backup
for /f %%i in (%tempfile%) do (
if exist backup\%backupdate%-%%i del %backupdate%-%%i
if exist %%i move %%i backup\%backupdate%-%%i
)

:download
for /f %%i in (%tempfile%) do (
wget -nv --no-check-certificate %vmurl%%%i
)

:converttolang
for /f %%i in (%tempfile%) do (
if exist %%~ni.lang del %%~ni.lang
if exist %%i trans.py %%i -e
)

:github
if "%giturl%"=="" goto svn
if not exist github md github
for /f %%i in (%tempfile%) do (
if exist github\%%i del github\%%i
wget -nv --no-check-certificate %giturl%%%i -O github\%%i
)
:svn
if "%svnurl%"=="" goto end
if not exist svn svn co %svnurl% svn
cd svn
svn up
cd ..
goto end


:notvmdir
echo This is not a valid Verbatim directory
echo Try creating it using vm init projectname
echo.
goto end

:init
if exist .verbatim goto initerror1
set prjname=%2
if "%prjname%"=="" goto initerror2
echo vmname==%prjname%> .verbatim
echo # The URL for downloading files from Verbatim >> .verbatim
echo vmurl==https://localize.mozilla.org/download/it/%prjname%/LC_MESSAGES/>> .verbatim
echo # The git URL for downloading the files, if available or none >> .verbatim
echo # giturl==https://raw.github.com/mozilla/%prjname%/master/locale/it/LC_MESSAGES/>> .verbatim
echo # If the project is stored on svn use svn url instead. >> .verbatim
echo # svnurl==https://svn.mozilla.org/projects/l10n-misc/trunk/%prjname%/locale/it/LC_MESSAGES/>>.verbatim
echo files==javascript.po,messages.po>> .verbatim
attrib +h .verbatim
echo Check the file .verbatim to verify that all is correct
echo Use attrib -H .verbatim to modify it, itt has been hidden.
echo.
goto end


:initerror1
echo This folder is already set for working with Verbatim.
echo if something not work as expected try editing the hidden file .verbatim or deleting it and launching the vm init command again.
echo To modify the file, you need to remove the hidden attribute with attrib: attrib -h .verbatim
echo.
goto end

:initerror2
echo To initialize a folder for working with Verbatim you need to specify the project name
echo See here for all available projects https://localize.mozilla.org/it/

:end
REM Reset all variables used.
set vmurl=
set giturl=
set svnurl=
set files=
if exist %tempfile% del %tempfile%
echo.