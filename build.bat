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
python -m eel main.py web --clean --noconfirm --onedir --windowed --icon icon.ico --name "Useful Tools for Windows"
cd "dist\Useful Tools for Windows\"
echo Zipping the portable edition...
7z a -r ..\..\..\dist\Useful_Tools_For_Windows_Portable.zip *
cd ..\..\..
echo Building the installer...
"%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" setup.iss
"%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" setup.iss
echo Cleaning up...
rmdir /s /q tmp
echo Done!
