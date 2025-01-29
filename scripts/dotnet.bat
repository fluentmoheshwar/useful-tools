@echo off
set ver=3.5
Title Microsoft .NET Framework %ver% Installer
for %%I in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do if exist "%%I:\\sources\install.wim" set setupdrv=%%I
if defined setupdrv (
echo Found drive %setupdrv%
echo Press any key to start the install...
pause > nul
echo Installing Microsoft .NET Framework %ver%...
dism /online /enable-feature /featurename:NetFX3 /All /Source:%setupdrv%:\sources\sxs /LimitAccess
echo Microsoft .NET Framework %ver% installed successfully.
) else (
    for %%I in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do if exist "%%I:\\sources\install.esd" set setupdrv=%%I
    if defined setupdrv (
    echo Found drive %setupdrv%
    echo Press any key to start the install...
    pause > nul
    echo Installing Microsoft .NET Framework %ver%...
    dism /online /enable-feature /featurename:NetFX3 /All /Source:%setupdrv%:\sources\sxs /LimitAccess
    echo Microsoft .NET Framework %ver% installed successfully.
    ) else (
        echo No Windows installation media found!
        echo Insert DVD or USB flash drive and run this file once again.
    )
)
echo Press any key to exit...
pause > nul
exit
