@echo off
mplayer  %1 -dumpstream
ren stream.dump %2