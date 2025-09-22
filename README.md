# LangChain RAG template 

Write-Host " Starting Project Setup..." -ForegroundColor Green

# ---------- Prerequisites Check ----------
function Check-Command {
    param([string]$cmd)
    if (!(Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host " $cmd not found. Please install it before continuing." -ForegroundColor Red
        exit 1
    }
    else {
        Write-Host " $cmd found." -ForegroundColor Cyan
    }
}

Check-Command "git"
Check-Command "dotnet"
Check-Command "python"
Check-Command "sqlcmd"

# ---------- Clone Repositories ----------
Write-Host " Cloning repositories..." -ForegroundColor Yellow

if (!(Test-Path "web-app")) {
    git clone https://github.com/GPAPD/web-app.git
} else {
    Write-Host " web-app already exists, skipping clone."
}

if (!(Test-Path "ai-assistant")) {
    git clone https://github.com/GPAPD/ai-assistant.git
} else {
    Write-Host " ai-assistant already exists, skipping clone."
}

# ---------- Database Restore ----------
Write-Host " Restoring Database RagDB..." -ForegroundColor Yellow
if (Test-Path "Rag.bkp") {
    sqlcmd -S localhost -Q "RESTORE DATABASE RagDB FROM DISK='$(Get-Location)\Rag.bkp' WITH REPLACE"
    Write-Host " Database restored as RagD
