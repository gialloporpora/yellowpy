@echo off
if "%2"=="" (set lines=3) else (set lines=%2)
set /a lines=%lines% + 1
echo %lines%
set sed="$q;N;%lines%,$D;ba"
sed -e :a -e %sed% %1