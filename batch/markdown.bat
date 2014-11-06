@echo off
set filename=%temp%\temp_markdown.html
if exist %filename% del %filename%
pandoc %1 -f markdown -t html5 --toc --standalone --self-contained --smart -o %filename%
start "" "%filename%



