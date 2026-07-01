Set WshShell = CreateObject("WScript.Shell")
' Get the current folder where this script is located
scriptdir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
' Run the start_validator.bat file completely hidden (0 means hidden window)
WshShell.Run chr(34) & scriptdir & "\start_validator.bat" & Chr(34), 0
Set WshShell = Nothing
