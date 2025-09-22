# ============================
# Project Setup Script
# ============================

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
    Write-Host " Database restored as RagDB" -ForegroundColor Cyan
} else {
    Write-Host " Rag.bkp not found. Please place it in the project root." -ForegroundColor Red
}

# ---------- Backend Setup ----------
Write-Host " Setting up Python environment..." -ForegroundColor Yellow
Set-Location ai-assistant

if (!(Test-Path "venv")) {
    python -m venv venv
    Write-Host " Virtual environment created."
} else {
    Write-Host " venv already exists, skipping."
}

.\venv\Scripts\Activate

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host " Dependencies installed."
} else {
    Write-Host "⚠ requirements.txt not found, skipping dependency install." -ForegroundColor Red
}

# Create .env if not exists
if (!(Test-Path ".env")) {
    Write-Host "PINECONE_API_KEY=your-pinecone-key" | Out-File -Encoding utf8 .env
    Add-Content .env "OPENAI_API_KEY=your-openai-key"
    Write-Host " Created .env file (please update keys)." -ForegroundColor Yellow
}

Set-Location ..

# ---------- Final Instructions ----------
Write-Host "`n Setup Completed!" -ForegroundColor Green
Write-Host " Next Steps:"
Write-Host "1. Open 'web-app' in Visual Studio 2022 and update appsettings.json with your connection string."
Write-Host "2. Start Backend: cd ai-assistant; .\venv\Scripts\Activate; py -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"
Write-Host "3. Start Frontend in Visual Studio."
Write-Host "4. Ensure Ollama llama3 is running locally."
