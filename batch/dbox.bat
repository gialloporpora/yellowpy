@echo off
set DBOXPUBLIC= c:\dropbox\public\
fsutil hardlink create  %DBOXPUBLIC%%~nx1  %1
echo %DBOXPUBLIC%%~nx1

