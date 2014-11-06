@echo off
call c:\python27\markdown\md.py %1 -o %temp%\temp.html
start %temp%\temp.html


