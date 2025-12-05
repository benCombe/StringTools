::@echo off
setlocal enabledelayedexpansion

:: Step 1: Search for "StringTools" folder inside "C:\Program Files"
set "programFilesPath=C:\Program Files"
set "stringToolsPath="

for /d %%D in ("%programFilesPath%\*") do (
    if exist "%%D\StringTools" (
        set "stringToolsPath=%%D\StringTools"
    )
)

:: If folder was not found, create it in C:\Program Files
if not defined stringToolsPath (
    set "stringToolsPath=%programFilesPath%\StringTools"
    echo StringTools folder not found. Creating "%stringToolsPath%" (Admin rights required)...
    mkdir "%stringToolsPath%" || (
        echo Failed to create folder. Run as Administrator.
        exit /b 1
    )
) else (
    echo StringTools folder found at "%stringToolsPath%".
)

:: Step 2: Copy files from the "dist" folder
set "sourceFolder=%~dp0dist"
set "destinationFolder=%stringToolsPath%"

echo Copying .exe files and 'words' folder...
copy "%sourceFolder%\wordfinder.exe" "%destinationFolder%" /Y
copy "%sourceFolder%\wordlesolver.exe" "%destinationFolder%" /Y

:: Copy the "words" folder and its contents
if exist "%sourceFolder%\words\" (
    xcopy "%sourceFolder%\words" "%destinationFolder%\words" /E /I /Y
)

echo Files copied successfully.

:: Step 3: Add StringTools to PATH if not already added
for /f "delims=" %%P in ('echo %PATH%') do (
    echo %%P | find /I "%stringToolsPath%" >nul && set "alreadyInPath=1"
)

if not defined alreadyInPath (
    echo Adding "%stringToolsPath%" to system PATH...
    setx PATH "%PATH%;%stringToolsPath%" /M
    echo PATH updated successfully.
) else (
    echo StringTools is already in PATH.
)

echo Installation complete!
pause
exit /b 0
