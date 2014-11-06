@ECHO OFF
path=%path%;%programfiles%\7-zip
ECHO Deep Archive
ECHO Written by: Jason Faulkner
ECHO SysadminGeek.com
ECHO.
ECHO.

REM Takes a Zip file and recompresses it as 7z archive.
REM Script process:
REM    1. Decompress the existing archive.
REM    2. Compress the extracted files in 7z format.
REM    3. (optional) Validate the new 7z file.
REM    4. (optional) Delete the source archive.
REM
REM Usage:
REM DeepArchive ZipFile
REM
REM Requirements:
REM    The 7-Zip command line tool (7za.exe) is in a location set in the PATH variable.
REM
REM Additional Notes:
REM This script processes a single zip archive.
REM To process all zip archives in a folder, use the ForFiles command from the command line:
REM    FORFILES /P "pathtozipfiles" /M *.zip /C "cmd /c DeepArchive @path"
REM
REM To run the archive compression/decompression as low priority background processes
REM add this in front of the 7ZA commands (DO NOT add this in front of the validation 7ZA command):
REM    START /BelowNormal /Wait 
REM Adding the above command will use a new window to perform these operations.

SETLOCAL EnableExtensions EnableDelayedExpansion

REM Should the deep archive file be validated? (1=yes, 0=no)
SET Validate=0

REM Compression level: 1,3,5,7,9 (higher=slower but more compression)
SET CompressLevel=5

REM Delete source zip file on success? (1=yes, 0=no)
SET DeleteSourceOnSuccess=1


REM ---- Do not modify anything below this line ----

SET ArchiveFile=%1
SET DeepFile=%ArchiveFile:.zip=.7z%
SET tmpPath=%TEMP%%~nx1
SET tmpPathZip="%tmpPath%*"
SET tmpPath="%tmpPath%"
SET tmpFile="%TEMP%tmpDeepArchive.txt"

IF NOT EXIST %tmpPath% (
   MKDIR %tmpPath%
) ELSE (
   RMDIR /S /Q %tmpPath%
)

ECHO Extracting archive: %ArchiveFile%
7Z x %ArchiveFile% -o%tmpPath%
ECHO.

ECHO Compressing archive: %DeepFile%
cd
pause
cd  %tmpPathZip%
7Z a -t7z -mx%CompressLevel% %DeepFile% 
ECHO.

IF {%Validate%}=={1} (
   ECHO Validating archive: %DeepFile%
   7Z t %DeepFile% | FIND /C "Everything is Ok" > %tmpFile%
   SET /P IsValid=< %tmpFile%
   IF !IsValid!==0 (
      ECHO Validation failed!
      DEL /F /Q %DeepFile%
      ECHO.
      GOTO Fail
   ) ELSE (
      ECHO Validation passed.
   )
   ECHO.
)
GOTO Success


:Success
IF {%DeleteSourceOnSuccess%}=={1} DEL /F /Q %ArchiveFile%
ECHO Success
GOTO End


:Fail
ECHO Failed
GOTO End


:End
IF EXIST %tmpFile% DEL /F /Q %tmpFile%
IF EXIST %tmpPath% RMDIR /S /Q %tmpPath%

ENDLOCAL