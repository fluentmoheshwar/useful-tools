@echo off
echo Cleaning up temporary files...

echo Cleaning Windows Temp folder...
del /s /q %windir%\Temp\*.*

echo Cleaning Windows SystemTemp folder...
del /s /q %windir%\SystemTemp\*.*

echo Cleaning User Temp folder...
del /s /q %temp%\*.*

echo Cleaning Windows Prefetch...
del /s /q %windir%\Prefetch\*.*

echo Cleaning Windows temporary files...
del /s /q %windir%\*.tmp
del /s /q %windir%\*._mp
del /s /q %windir%\*.log
del /s /q %windir%\*.gid
del /s /q %windir%\*.chk
del /s /q %windir%\*.old

echo Cleaning Recent Documents...
del /s /q %userprofile%\Recent\

echo Cleanup completed! Please use storage sense to remove additional temporary files.
explorer.exe ms-settings:storagesense
pause
