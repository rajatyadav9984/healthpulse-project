Set WinScriptHost = CreateObject("WScript.Shell")
strPath = WScript.Arguments(0)
WinScriptHost.Run Chr(34) & strPath & Chr(34), 0
Set WinScriptHost = Nothing
