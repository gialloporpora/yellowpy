@echo off
openssl md5 %1 > %1.txt
openssl sha1 %1 >> %1.txt
openssl dgst -sha256 %1 >> %1.txt
echo ----------------------------------------------------------------------------------------
echo MD5 and Sha1 digest saved in %1.txt
type %1.txt
echo ----------------------------------------------------------------------------------------
echo.