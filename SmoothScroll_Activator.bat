@echo off
setlocal enabledelayedexpansion

for /f %%a in ('powershell -command "(Get-Date).ToUniversalTime().Subtract((Get-Date "1970-01-01")).TotalSeconds"') do set "timestamp=%%a"
echo %timestamp%
set /a "timestamp=timestamp/1"
echo %timestamp%

chcp 1251

set "subKey=Software\SmoothScroll"
set "valueName=kSSInstallDate"
set "valueData=!timestamp!"

reg add "HKCU\%subKey%" /v "%valueName%" /t REG_SZ /d "%valueData%" /f > nul 2>&1

endlocal
