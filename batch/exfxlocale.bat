@echo off
set dest=%~1
IF NOT EXIST "%dest%" goto errore
md %temp%\firefox\base
md %temp%\firefox\browser
md %temp%\firefox\metro
md %temp%\firefox\webapprt
unzip -qq omni.ja -d "%temp%\firefox\base"
unzip -qq browser\omni.ja -d "%temp%\firefox\browser"
unzip -qq metro\omni.ja -d "%temp%\firefox\metro"
unzip -qq webapprt\omni.ja -d "%temp%\firefox\webapprt"
sed -n "/^locale global .*/{s/^locale global \([a-zA-Z-]*\).*/\1/;p}" %temp%\firefox\base\chrome\chrome.manifest > %temp%\firefox\locale.txt
for /f %%i in (%temp%\firefox\locale.txt) do set fxlocale=%%i
echo %fxlocale%
md %temp%\firefox\%fxlocale%\base
md %temp%\firefox\%fxlocale%\browser
md %temp%\firefox\%fxlocale%\metro
md %temp%\firefox\%fxlocale%\webapprt
cls
xcopy  /Q /E %temp%\firefox\base\chrome\%fxlocale%\locale\%fxlocale% %temp%\firefox\%fxlocale%\base
xcopy /Q /E %temp%\firefox\browser\chrome\%fxlocale%\locale %temp%\firefox\%fxlocale%\browser
xcopy /Q /E %temp%\firefox\metro\chrome\%fxlocale%\locale %temp%\firefox\%fxlocale%\metro
xcopy /Q /E %temp%\firefox\webapprt\chrome\%fxlocale%\locale\webapprt %temp%\firefox\%fxlocale%\webapprt


dir /b/s %temp%\firefox\%fxlocale%\*.dtd > %temp%\firefox\files.txt
dir /b/s %temp%\firefox\%fxlocale%\*.properties >> %temp%\firefox\files.txt
set sed="h;s/.*\\\\firefox\\\\%fxlocale%\\\\\(.*\)/\1/;s/\\\\/_____/g;G;s/\n/==/"
sed %sed% %temp%\firefox\files.txt > %temp%\firefox\newfiles.txt
md %temp%\firefox\%fxlocale%-unified
FOR /F "delims=== tokens=1,2" %%i in (%temp%\firefox\newfiles.txt) do move "%%j" "%temp%\firefox\%fxlocale%-unified\%%i"
md %temp%\firefox\%fxlocale%-po
path=%path%;c:\python27\scripts
moz2po.py -i %temp%\firefox\%fxlocale%-unified   -o %temp%\firefox\%fxlocale%-po
md "%dest%\%fxlocale%-unified"
md "%dest%\%fxlocale%-po"
xcopy /E /Q %temp%\firefox\%fxlocale%-unified "%dest%\%fxlocale%-unified"
xcopy /E /Q %temp%\firefox\%fxlocale%-po "%dest%\%fxlocale%-po"
rd /s /q %temp%\firefox
echo Ok, tutto sembra a posto :-), ma non si sa mai :-P
goto fine


:errore
echo Devi specificare un percorso valido, grazie.



:fine
