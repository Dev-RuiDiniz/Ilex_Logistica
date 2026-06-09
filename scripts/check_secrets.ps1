# Script de verificação de secrets no código (PowerShell)
# Wrapper que chama a mesma lógica Python do Bash

# Resolver raiz do repositório
$ScriptPath = $PSScriptRoot
$RepoRoot = Split-Path -Parent $ScriptPath

# Mudar para a raiz do repositório
Set-Location $RepoRoot

# Localizar Python
$PythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $PythonCmd = $cmd
        break
    }
}

if (-not $PythonCmd) {
    Write-Host "ERROR: Python not found"
    exit 1
}

# Executar script Python com repo root
& $PythonCmd scripts/check_secrets.py --repo-root $RepoRoot $args
exit $LASTEXITCODE
