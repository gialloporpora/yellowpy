@echo off

set file=%1
sed -n "H;${x;s/\n//g;s/.*/javascript:(function(){&})();/;p}" %file%

