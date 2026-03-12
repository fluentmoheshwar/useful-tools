# pyright: reportMissingImports=false, reportMissingModuleSource=false, reportUnknownParameterType=false, reportMissingParameterType=false, reportUnknownVariableType=false, reportMissingTypeArgument=false, reportFunctionMemberAccess=false, reportUnnecessaryIsInstance=false, reportAttributeAccessIssue=false, reportUnknownMemberType=false, reportUnknownArgumentType=false, reportCallIssue=false, reportUnusedImport=false, reportUnnecessaryComparison=false
from typing import Any, cast, Callable, Dict, List, Sequence, Tuple
from types import ModuleType

# Imports eel, An Electron like GUI for Python.
try:
    import eel
except Exception:
    # Minimal stub for testing environments without eel installed.
    class _EelStub:
        def init(self, *a: Any, **k: Any) -> None:
            return None

        def expose(self, f: Callable[..., Any] | None = None) -> Any:
            if f is None:
                def _decorator(func: Callable[..., Any]) -> Callable[..., Any]:
                    return func

                return _decorator
            return f

        def start(self, *a: Any, **k: Any) -> None:
            return None

    eel = _EelStub()

# Initializes eel
eel.init("web")

# Tell static type checkers that `eel` is dynamic so we can attach runtime
# attributes like `_real_expose` and `_already_exposed` without Pylance errors.
eel = cast(Any, eel)

# Replace eel.expose with a lightweight deferred registrator so decorating
# many functions is cheap at import time. The real eel.expose (if present)
# is saved to `eel._real_expose` and the deferred wrapper stores functions
# in `eel._deferred_expose_registry` to be actually exposed later by
# `expose_all()` which runs once at startup.
_real_expose = getattr(eel, "expose", None)

_deferred_expose_registry: List[Callable[..., Any]] = []

def _make_deferred_expose(real):
    def expose(func=None):
        # Used both as `@eel.expose` and `eel.expose(func)`.
        if func is None:
            def _decorator(f):
                _deferred_expose_registry.append(f)
                return f

            return _decorator
        _deferred_expose_registry.append(func)
        return func

    return expose

# Install the deferred wrapper on eel so existing `@eel.expose` uses it.
eel.expose = _make_deferred_expose(_real_expose)
eel._deferred_expose_registry = _deferred_expose_registry
eel._real_expose = _real_expose
eel._already_exposed = set()


import shlex
import subprocess
import sys
import re
from typing import Union, List, Optional, Dict


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


def _validate_cmd(cmd: Union[str, List[str], Tuple[str, ...]]):
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
    cmd: Union[str, List[str], Tuple[str, ...]],
    timeout: Optional[float] = None,
    check: bool = False,
    capture_output: bool = False,
    text: bool = True,
) -> subprocess.CompletedProcess[Any]:
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


def expose_all(module: Optional[ModuleType] = None, include_private: bool = False, exclude: Optional[Union[List[str], Tuple[str, ...]]] = None) -> int:
    """Automatically expose top-level functions from a module to eel.

    Args:
        module: module object to scan. If None, uses the current module.
        include_private: whether to include names starting with '_'.
        exclude: iterable of names to exclude.

    Returns:
        The number of functions successfully exposed.

    Raises:
        TypeError: if arguments are of incorrect type.
    """
    import inspect
    import sys

    if exclude is not None and not isinstance(exclude, (list, tuple, set)):
        raise TypeError("exclude must be a list, tuple, set, or None")

    # Normalize module parameter and ensure it's a ModuleType so static
    # checkers know `__name__` exists.
    if module is None:
        mod = sys.modules[__name__]
    else:
        if not isinstance(module, ModuleType):
            raise TypeError("module must be a module object")
        mod = module

    exposed = 0

    if not callable(getattr(eel, "expose", None)):
        # If `eel.expose` is not callable at all, there is nothing to do,
        # but the deferred registry or `_real_expose` may still be present.
        pass

    # Determine exposer: prefer the real underlying expose (set at import time),
    # otherwise fall back to whatever is currently on `eel.expose`.
    real_expose = getattr(eel, "_real_expose", None)
    current_expose = getattr(eel, "expose", None)

    # Collect candidate functions: top-level functions in the module
    members: Dict[str, Callable[..., Any]] = {
        name: obj
        for name, obj in inspect.getmembers(mod, inspect.isfunction)
        if obj.__module__ == mod.__name__
    }

    # If decorators used the deferred wrapper, include those registered functions
    deferred_registry = getattr(eel, "_deferred_expose_registry", None)
    if deferred_registry:
        for f in deferred_registry:
            members.setdefault(f.__name__, f)

    # Exposer to call when actually registering functions with eel runtime.
    exposer: Any = real_expose or current_expose
    if not callable(exposer):
        return exposed
    # Cast to Any for strict type-checking so calls don't raise call-issue errors
    callable_exposer = cast(Any, exposer)

    already = getattr(eel, "_already_exposed", set())

    for name, obj in members.items():
        if not include_private and name.startswith("_"):
            continue
        if exclude and name in exclude:
            continue

        key = f"{mod.__name__}.{name}"
        if key in already:
            continue

        try:
            # real exposer may accept a function directly or return a decorator
            result = callable_exposer(obj)
            if callable(result) and result is not obj:
                # exposer returned a decorator — apply it
                result(obj)
        except TypeError:
            try:
                callable_exposer()(obj)
            except Exception:
                # If exposing fails for a function, skip it but don't crash
                continue

        already.add(key)
        exposed += 1

    setattr(eel, "_already_exposed", already)

    return exposed


# sudo setup
def gsudo():
    run_command("winget install gerardog.gsudo")


# Files and folders
def openHosts():
    run_command(
        'sudo cmd.exe /c "attrib -r %WINDIR%\\system32\\drivers\\etc\\hosts && notepad.exe %WINDIR%\\system32\\drivers\\etc\\hosts"'
    )


def openOfficeAddins():
    run_command("explorer.exe %AppData%\\Microsoft\\AddIns")


def openCurrentUserStartMenu():
    run_command("explorer.exe %AppData%\\Microsoft\\Windows\\Start Menu")


def openAllUserStartMenu():
    run_command("explorer.exe C:\\ProgramData\\Microsoft\\Windows\\Start Menu")


def openSentTo():
    run_command("explorer.exe %Appdata%\\Microsoft\\Windows\\SendTo")


def openCurrentUserStartup():
    run_command(
        "explorer.exe %AppData%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    )


def openAllUsersStartup():
    run_command(
        "explorer.exe C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp"
    )


def openWordStartup():
    run_command("explorer.exe %AppData%\\Microsoft\\Word\\STARTUP")


def openPSReadLineHistory():
    run_command(
        "notepad %AppData%\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt"
    )


def openAccountPictures():
    run_command("explorer shell:AccountPictures")


def openVirtualDisks():
    run_command("explorer %ProgramData%\\Microsoft\\Windows\\Virtual Hard Disks")


def openApplicationsFolder():
    run_command("explorer shell:AppsFolder")


def superGodMode():
    run_command(
        'powershell -Command "irm https://cdn.jsdelivr.net/gh/ThioJoe/Windows-Super-God-Mode@main/Super_God_Mode.ps1 | iex"'
    )


# Settings and Utilities
def openFolderOptions():
    run_command("explorer shell:::{6DFD7C5C-2451-11d3-A299-00C04F8EF6AF}")


def openInternetOptions():
    run_command("explorer shell:::{A3DD4F92-658A-410F-84FD-6FBBBEF2FFFE}")


def openSoundOptions():
    run_command("explorer shell:::{F2DDFC82-8F12-4CDD-B7DC-D4FE1425AA4D}")


def openPowerOptions():
    run_command("explorer shell:::{025A5937-A6BE-4686-A844-36FE4BEC8B6D}")


def openOptionalFeatures():
    run_command("start %WINDIR%\\System32\\OptionalFeatures.exe")


def openControlPanel():
    run_command("start control.exe")


def openGodMode():
    run_command("explorer.exe shell:::{ed7ba470-8e54-465e-825c-99712043e01c}")


def openTaskManager():
    run_command("taskmgr")


def openTaskManagerEight():
    run_command("taskmgr -d")


def openTaskManagerXP():
    run_command("sudo scripts\\taskmgr.exe")


def openmsconfig():
    run_command("msconfig")


def openPersonalization():
    run_command("explorer shell:::{ED834ED6-4B5A-4bfe-8F11-A626DCB6A921}")


def openmsconfigXP():
    run_command("sudo scripts\\msconfig.exe")


def fKeySender():
    import requests # Local import to avoid adding requests as a dependency for the whole app since it's only used in this one function.

    response = requests.get(
        "https://api.github.com/repos/ThioJoe/F-Key-Sender/releases/latest"
    ).json()
    url = response["assets"][0]["browser_download_url"]
    run_command(
        f"powershell -Command Start-BitsTransfer -Source {url} -Destination $env:TEMP && %TEMP%\\F_Key_Sender.exe"
    )


def titusWinutil():
    run_command('sudo powershell -Command "irm https://christitus.com/win | iex"')


def dotnetInstaller():
    run_command('sudo cmd.exe /c "scripts\\dotnet.bat"')


def updatePrograms():
    run_command("winget upgrade --all")


# Repair Tools
def shutdown():
    run_command("shutdown /s /t 0")


def restart():
    run_command("shutdown /r /t 0")


def restartToFirmware():
    run_command("sudo shutdown /r /fw /t 0")


def repairSystemFiles():
    run_command("sudo sfc /scannow && pause")


def repairWindowsComponents():
    run_command("sudo dism /online /cleanup-image /restorehealth && pause")


def wsreset():
    run_command("sudo wsreset.exe")


def flushDNS():
    run_command("ipconfig /flushdns")


def restartWinNat():
    run_command('sudo cmd.exe /c "net stop winnat && net start winnat"')


def winsockFix():
    run_command("sudo netsh winsock reset")


def killNotRespondingApps():
    run_command('sudo taskkill.exe /F /FI "status eq NOT RESPONDING" && pause')


def cleanupTempFiles():
    run_command("sudo scripts\\cleanuptemp.bat")


if __name__ == "__main__":
    # Expose functions to eel once at startup and print a short example output.
    try:
        count = expose_all()
    except Exception:
        count = 0
    print(f"Exposed {count} functions to eel")
    eel.start("index.html", mode="edge")
