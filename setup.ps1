if (Test-Path .\.virtualenv) {
    Remove-Item -Recurse -Force .\.virtualenv
}

python -m venv .\.virtualenv
.\.virtualenv\Scripts\Activate.ps1
python -m pip install --upgrade pip

if (Test-Path .\requirements.txt) {
    pip install -r requirements.txt
} else {
    Write-Host "Warning: requirments.txt bnot found. Skipping dependecies installation."
}

Write-Host "Enviornment setup complete. Virtual environment is now active."