# Imports eel, An Electron like GUI for Python.
try:
    import eel
except Exception:
    # Minimal stub for testing environments without eel installed.
    class _EelStub:
        def init(self, *a, **k):
            return None

        def expose(self, f=None):
            if f is None:
                def _decorator(func):
                    return func

                return _decorator
            return f

        def start(self, *a, **k):
            return None

    eel = _EelStub()

# Initializes eel
eel.init("web")


import shlex
import subprocess
import sys
import re
from typing import Union, List, Optional


def _needs_shell_for_string(cmd: str) -> bool:
    if not cmd:
        return False
    shell_tokens = ["&&", "||", "|", ">", "<", ";", "&"]
    if any(tok in cmd for tok in shell_tokens):
        return True
    if "%" in cmd and re.search(r"%[^%]+%", cmd):
        return True
    if re.search(r"\b(cmd\.exe|powershell|start|sudo|gsudo)\b", cmd, flags=re.I):
        return True
    return False


def _validate_cmd(cmd: Union[str, List[str], tuple]):
    if cmd is None:
        raise ValueError("cmd must be a non-empty string or a list of strings")
    if isinstance(cmd, (list, tuple)):
        if len(cmd) == 0:
            raise ValueError("cmd list must not be empty")
        for i, part in enumerate(cmd):
            if not isinstance(part, str):
                raise TypeError(f"cmd list element at index {i} is not a string")
    elif isinstance(cmd, str):
        if cmd.strip() == "":
            raise ValueError("cmd must not be an empty string")
    else:
        raise TypeError("cmd must be a string or a list/tuple of strings")


def run_command(
    cmd: Union[str, List[str]],
    timeout: Optional[float] = None,
    check: bool = False,
    capture_output: bool = False,
    text: bool = True,
) -> subprocess.CompletedProcess:
    _validate_cmd(cmd)
    shell = False
    run_args = cmd
    if isinstance(cmd, str):
        shell = _needs_shell_for_string(cmd)
        if not shell:
            try:
                run_args = shlex.split(cmd, posix=not sys.platform.startswith("win"))
            except Exception:
                shell = True
    return subprocess.run(
        run_args,
        shell=shell,
        timeout=timeout,
        check=check,
        capture_output=capture_output,
        text=text,
    )


# sudo setup
@eel.expose
def gsudo():
    run_command("winget install gerardog.gsudo")


# Files and folders
@eel.expose
def openHosts():
    run_command(
        'sudo cmd.exe /c "attrib -r %WINDIR%\\system32\\drivers\\etc\\hosts && notepad.exe %WINDIR%\\system32\\drivers\\etc\\hosts"'
    )


@eel.expose
def openOfficeAddins():
    run_command("explorer.exe %AppData%\\Microsoft\\AddIns")


@eel.expose
def openCurrentUserStartMenu():
    run_command("explorer.exe %AppData%\\Microsoft\\Windows\\Start Menu")


@eel.expose
def openAllUserStartMenu():
    run_command("explorer.exe C:\\ProgramData\\Microsoft\\Windows\\Start Menu")


@eel.expose
def openSentTo():
    run_command("explorer.exe %Appdata%\\Microsoft\\Windows\\SendTo")


@eel.expose
def openCurrentUserStartup():
    run_command(
        "explorer.exe %AppData%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    )


@eel.expose
def openAllUsersStartup():
    run_command(
        "explorer.exe C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp"
    )


@eel.expose
def openWordStartup():
    run_command("explorer.exe %AppData%\\Microsoft\\Word\\STARTUP")


@eel.expose
def openPSReadLineHistory():
    run_command(
        "notepad %AppData%\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt"
    )


@eel.expose
def openAccountPictures():
    run_command("explorer shell:AccountPictures")


@eel.expose
def openVirtualDisks():
    run_command("explorer %ProgramData%\\Microsoft\\Windows\\Virtual Hard Disks")


@eel.expose
def openApplicationsFolder():
    run_command("explorer shell:AppsFolder")


@eel.expose
def superGodMode():
    run_command(
        'powershell -Command "irm https://cdn.jsdelivr.net/gh/ThioJoe/Windows-Super-God-Mode@main/Super_God_Mode.ps1 | iex"'
    )


# Settings and Utilities
@eel.expose
def openFolderOptions():
    run_command("explorer shell:::{6DFD7C5C-2451-11d3-A299-00C04F8EF6AF}")


@eel.expose
def openInternetOptions():
    run_command("explorer shell:::{A3DD4F92-658A-410F-84FD-6FBBBEF2FFFE}")


@eel.expose
def openSoundOptions():
    run_command("explorer shell:::{F2DDFC82-8F12-4CDD-B7DC-D4FE1425AA4D}")


@eel.expose
def openPowerOptions():
    run_command("explorer shell:::{025A5937-A6BE-4686-A844-36FE4BEC8B6D}")


@eel.expose
def openOptionalFeatures():
    run_command("start %WINDIR%\\System32\\OptionalFeatures.exe")


@eel.expose
def openControlPanel():
    run_command("start control.exe")


@eel.expose
def openGodMode():
    run_command("explorer.exe shell:::{ed7ba470-8e54-465e-825c-99712043e01c}")


@eel.expose
def openTaskManager():
    run_command("taskmgr")


@eel.expose
def openTaskManagerEight():
    run_command("taskmgr -d")


@eel.expose
def openTaskManagerXP():
    run_command("sudo scripts\\taskmgr.exe")


@eel.expose
def openmsconfig():
    run_command("msconfig")


@eel.expose
def openPersonalization():
    run_command("explorer shell:::{ED834ED6-4B5A-4bfe-8F11-A626DCB6A921}")


@eel.expose
def openmsconfigXP():
    run_command("sudo scripts\\msconfig.exe")


@eel.expose
def fKeySender():
    import requests # Local import to avoid adding requests as a dependency for the whole app since it's only used in this one function.

    response = requests.get(
        "https://api.github.com/repos/ThioJoe/F-Key-Sender/releases/latest"
    ).json()
    url = response["assets"][0]["browser_download_url"]
    run_command(
        f"powershell -Command Start-BitsTransfer -Source {url} -Destination $env:TEMP && %TEMP%\\F_Key_Sender.exe"
    )


@eel.expose
def titusWinutil():
    run_command('sudo powershell -Command "irm https://christitus.com/win | iex"')


@eel.expose
def dotnetInstaller():
    run_command('sudo cmd.exe /c "scripts\\dotnet.bat"')


@eel.expose
def updatePrograms():
    run_command("winget upgrade --all")


# Repair Tools
@eel.expose
def shutdown():
    run_command("shutdown /s /t 0")


@eel.expose
def restart():
    run_command("shutdown /r /t 0")


@eel.expose
def restartToFirmware():
    run_command("sudo shutdown /r /fw /t 0")


@eel.expose
def repairSystemFiles():
    run_command("sudo sfc /scannow && pause")


@eel.expose
def repairWindowsComponents():
    run_command("sudo dism /online /cleanup-image /restorehealth && pause")


@eel.expose
def wsreset():
    run_command("sudo wsreset.exe")


@eel.expose
def flushDNS():
    run_command("ipconfig /flushdns")


@eel.expose
def restartWinNat():
    run_command('sudo cmd.exe /c "net stop winnat && net start winnat"')


@eel.expose
def winsockFix():
    run_command("sudo netsh winsock reset")


@eel.expose
def killNotRespondingApps():
    run_command('sudo taskkill.exe /F /FI "status eq NOT RESPONDING" && pause')


@eel.expose
def cleanupTempFiles():
    run_command("sudo scripts\\cleanuptemp.bat")


if __name__ == "__main__":
    eel.start("index.html", mode="edge")
