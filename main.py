# Imports system commands
import os

# Imports eel, a Electron like GUI for Python.
import eel

eel.init("web")

# Fixes Chrome not installed.
eel.browsers.set_path(
    "chrome", "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
)


@eel.expose
def openHosts():
    os.system(
        "attrib -r %WINDIR%\system32\drivers\etc\hosts && start notepad.exe %windir%\system32\drivers\etc\hosts"
    )


@eel.expose
def openOfficeAddins():
    os.system("explorer.exe %AppData%\Microsoft\AddIns")


@eel.expose
def openCurrentUserStartMenu():
    os.system("explorer.exe %AppData%\Microsoft\Windows\Start Menu")


@eel.expose
def openAllUserStartMenu():
    os.system("explorer.exe C:\ProgramData\Microsoft\Windows\Start Menu")


@eel.expose
def openSentTo():
    os.system("explorer.exe %Appdata%\Microsoft\Windows\SendTo")


@eel.expose
def openCurrentUserStartup():
    os.system("explorer.exe %AppData%\Microsoft\Windows\Start Menu\Programs\Startup")


@eel.expose
def openAllUsersStartup():
    os.system(
        "explorer.exe C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
    )


@eel.expose
def openWordStartup():
    os.system("explorer.exe %AppData%\Microsoft\Word\STARTUP")


@eel.expose
def openPSReadLineHistory():
    os.system(
        "notepad %AppData%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt"
    )


@eel.expose
def installYouTubeDownloader():
    os.system("winget install MoheshwarAmarnathBiswas.YouTubeVideoDownloader")


@eel.expose
def installPowerToys():
    os.system("winget install Microsoft.PowerToys")


@eel.expose
def installSysInternals():
    os.system("winget install --id 9P7KNL5RWT25")


eel.start("index.html")
