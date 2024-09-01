# https://stackoverflow.com/a/75242885/18629676
import sys, io

buffer = io.StringIO()
sys.stdout = sys.stderr = buffer

# Imports system commands
import os

# import requests
import requests

# Imports eel, An Electron like GUI for Python.
import eel

eel.init("web")

# Replaces Google Chrome with Microsoft Edge.
eel.browsers.set_path(
    "chrome", "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
)


# sudo setup


@eel.expose
def winSudo():
    os.system("sudo config --enable normal")


@eel.expose
def gsudo():
    os.system("winget install gerardog.gsudo")


# Files and folders
@eel.expose
def openHosts():
    os.system(
        "sudo attrib -r %WINDIR%\\system32\\drivers\\etc\\hosts && start notepad.exe %windir%\\system32\\drivers\\etc\\hosts"
    )


@eel.expose
def openOfficeAddins():
    os.system("explorer.exe %AppData%\\Microsoft\\AddIns")


@eel.expose
def openCurrentUserStartMenu():
    os.system("explorer.exe %AppData%\\Microsoft\\Windows\\Start Menu")


@eel.expose
def openAllUserStartMenu():
    os.system("explorer.exe C:\\ProgramData\\Microsoft\\Windows\\Start Menu")


@eel.expose
def openSentTo():
    os.system("explorer.exe %Appdata%\\Microsoft\\Windows\\SendTo")


@eel.expose
def openCurrentUserStartup():
    os.system(
        "explorer.exe %AppData%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    )


@eel.expose
def openAllUsersStartup():
    os.system(
        "explorer.exe C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp"
    )


@eel.expose
def openWordStartup():
    os.system("explorer.exe %AppData%\\Microsoft\\Word\\STARTUP")


@eel.expose
def openPSReadLineHistory():
    os.system(
        "notepad %AppData%\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt"
    )


@eel.expose
def openAccountPictures():
    os.system("explorer shell:AccountPictures")


@eel.expose
def openVirtualDisks():
    os.system("explorer %ProgramData%\\Microsoft\\Windows\\Virtual Hard Disks")


@eel.expose
def openApplicationsFolder():
    os.system("explorer shell:AppsFolder")


@eel.expose
def superGodMode():
    os.system(
        'powershell -Command "irm https://raw.githubusercontent.com/ThioJoe/Windows-Super-God-Mode/main/Super_God_Mode.ps1 | iex"'
    )


# Settings and Utilities
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
    os.system("start %WINDIR%\\System32\\OptionalFeatures.exe")


@eel.expose
def openControlPanel():
    os.system("start control.exe")


@eel.expose
def openGodMode():
    os.system("explorer.exe shell:::{ed7ba470-8e54-465e-825c-99712043e01c}")


# Repair Tools
@eel.expose
def shutdown():
    os.system("shutdown /s /t 0")


@eel.expose
def restart():
    os.system("shutdown /r /t 0")


@eel.expose
def repairSystemFiles():
    os.system("sudo sfc /scannow")


@eel.expose
def repairWindowsComponents():
    os.system("sudo dism /online /cleanup-image /restorehealth")


@eel.expose
def wsreset():
    os.system("sudo wsreset.exe")


@eel.expose
def restartWinNat():
    os.system("sudo net stop winnat && sudo net start winnat")


@eel.expose
def fKeySender():
    response = requests.get(
        "https://api.github.com/repos/ThioJoe/F-Key-Sender/releases/latest"
    ).json()
    url = response["assets"][0]["browser_download_url"]
    os.system(
        f"powershell -Command Start-BitsTransfer -Source {url} -Destination $env:TEMP && %TEMP%\\F_Key_Sender.exe"
    )


eel.start("index.html")
