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


@eel.expose
def openAccountPictures():
    os.system("explorer shell:AccountPictures")


@eel.expose
def openFolderOptions():
    os.system("explorer shell:::{6DFD7C5C-2451-11d3-A299-00C04F8EF6AF}")


@eel.expose
def openInternetOptions():
    os.system("explorer shell:::{A3DD4F92-658A-410F-84FD-6FBBBEF2FFFE}")


@eel.expose
def openSoundOptions():
    os.system("explorer shell:::{F2DDFC82-8F12-4CDD-B7DC-D4FE1425AA4D}")


@eel.expose
def openPowerOptions():
    os.system("explorer shell:::{025A5937-A6BE-4686-A844-36FE4BEC8B6D}")


@eel.expose
def openOptionalFeatures():
    os.system("start %WINDIR%\System32\OptionalFeatures.exe")


@eel.expose
def openControlPanel():
    os.system("start control.exe")


@eel.expose
def wsreset():
    os.system("start wsreset.exe")


@eel.expose
def wureset():
    os.system("net stop bits")
    os.system("net stop wuauserv")
    os.system("net stop CryptSvc")
    os.system("net stop msiserver")
    os.system("del %windir%\SoftwareDistribution")
    os.system("del %windir%\system32\catroot2")
    os.system("net start bits")
    os.system("net start wuauserv")
    os.system("net start CryptSvc")
    os.system("net start msiserver")


eel.start("index.html")
