# Build Lazerbeam Executable
Write-Host "Building Lazerbeam with PyInstaller..."

# Clean old builds
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }

# Run PyInstaller
..\.venv\Scripts\pyinstaller.exe --noconfirm --onedir --windowed --icon "icon.ico" --name "Lazerbeam" --collect-all "customtkinter" "..\app.py"

# Copy the icon next to the executable so pystray can find it at runtime, or we bundle it.
# For a 1-folder build (--onedir), we can just copy it:
Copy-Item "..\icon.ico" -Destination "dist\Lazerbeam\"

Write-Host "Build complete! Executable is in dist\Lazerbeam\Lazerbeam.exe"
