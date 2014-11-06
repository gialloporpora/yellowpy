]echo off
ffmpeg -i %1 -f avi -vcodec mpeg4 -b 800k -g 300 -bf 2 -acodec libmp3lame -ab 192k  %~n1.avi