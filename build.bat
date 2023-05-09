@echo off
"%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" setup.iss
cd tmp/dist
copy Useful_Tools_for_Windows_Portable.exe ..\..\dist\Useful_Tools_for_Windows_Portable.exe
