@echo off
set null="%~dp0null"

echo %null%
set tempfile=ssltmp.txt
echo %tempfile%
set domain=%~1
REM Download certificate from a domaina
echo Download certificate from %domain%
echo.


openssl s_client -connect "%domain%:443"   < %null%>>%tempfile%

echo.