@echo off
openssl dgst -sha224 %1 > "%~1.txt"
openssl dgst -sha256 %1 >> "%~1.txt"
openssl dgst -sha256 %1 >> "%~1.txt"
openssl dgst -sha384 %1 >> "%~1.txt"
openssl dgst -sha512 %1 >> "%~1.txt"