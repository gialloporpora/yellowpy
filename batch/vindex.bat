@echo off
mencoder %1 -o reindexed%1  -forceidx -oac copy -ovc copy