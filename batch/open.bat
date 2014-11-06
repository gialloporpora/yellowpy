@echo off
set filename=%~1
if exist "%filename%" ("c:\programmi\crimson editor\cedt.exe" "%filename%") else (echo File not found)