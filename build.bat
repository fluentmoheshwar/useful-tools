@echo off
echo Installing Inno Setup...
winget install --id=JRSoftware.InnoSetup -e -s winget
echo Installing Dependencies...
bun install
pip install uv
uv pip install git+https://github.com/bottlepy/bottle.git
uv pip install wheel
uv pip install -r requirements.txt
echo Building the UI...
bun run build
copy main.py tmp && copy icon.ico tmp
echo Building the executable folder...
cd tmp
pyinstaller --clean --noconfirm --onedir --windowed --icon icon.ico --name "Useful Tools for Windows" --add-data "web;web/" main.py
pyinstaller --clean --noconfirm --onefile --windowed --icon icon.ico --name "Useful_Tools_for_Windows_Portable" --add-data "web;web/" main.py
cd ..
echo Building the installer...
"%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" setup.iss
"%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" setup.iss
move .\tmp\dist\Useful_Tools_for_Windows_Portable.exe .\dist\Useful_Tools_for_Windows_Portable.exe
rmdir /s /q tmp
