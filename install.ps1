Write-Host "Installing todocli..."

$InstallDir = "$HOME\.local\bin"

if (!(Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force
}

Copy-Item "$PSScriptRoot\todocli" "$InstallDir\todocli" -Force
Copy-Item "$PSScriptRoot\todocli.cmd" "$InstallDir\todocli.cmd" -Force

$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($CurrentPath -notlike "*$InstallDir*") {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$CurrentPath;$InstallDir",
        "User"
    )
}

Write-Host "todocli installed successfully"
Write-Host "Restart terminal to use todocli"