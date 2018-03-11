# Remove build/dist
Remove-Item -Path 'build' -Recurse -Force
Remove-Item -Path 'dist'  -Recurse -Force

# Create the source distribution
Write-Host "Creating source dist"
Start-Process python -ArgumentList 'setup.py', 'sdist' -Wait -NoNewWindow

# Build the wheel
Write-Host "Building the wheel"
Start-Process pip -ArgumentList 'install', 'wheel' -Wait -NoNewWindow
Start-Process python -ArgumentList 'setup.py', 'bdist_wheel', '--universal' -Wait -NoNewWindow

# Upload the project to PyPi
Write-Host "Uploading to PyPi"
Start-Process twine -ArgumentList 'upload', 'dist/*' -Wait -NoNewWindow