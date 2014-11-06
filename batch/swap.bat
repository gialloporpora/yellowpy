@echo off
move %1 temp.backup1
move %2 temp.backup2
move temp.backup1 %2
move temp.backup2 %1


