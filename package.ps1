# Create the source distribution
Write-Host "Creating source dist"
Start-Process python -ArgumentList 'setup.py', 'sdist' -Wait

# Build the wheel
Write-Host "Building the wheel"
Start-Process pip -ArgumentList 'install', 'wheel' -Wait
Start-Process python -ArgumentList 'setup.py', 'bdist_wheel', '--universal' -Wait

# Upload the project to PyPi
Write-Host "Uploading to PyPi"
Start-Process twine -ArgumentList 'upload', 'dist/*' -Wait