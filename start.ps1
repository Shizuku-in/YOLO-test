$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  YOLO Monitoring System - Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found, please install Python 3.8+" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".env")) {
    Write-Host "[INFO] .env file not found, copying from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] .env file created" -ForegroundColor Green
    Write-Host ""
}

Write-Host "[INFO] Checking dependencies..." -ForegroundColor Cyan
try {
    pip show ultralytics | Out-Null
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "[INFO] Dependencies not installed, installing..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Dependencies installed successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "[INFO] Starting services..." -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

Write-Host "[1/3] Starting WebSocket server..." -ForegroundColor Yellow
$serverJob = Start-Process -FilePath "python" -ArgumentList "server.py" -WindowStyle Normal -PassThru
Start-Sleep -Seconds 2

Write-Host "[2/3] Starting YOLO detector..." -ForegroundColor Yellow
$detectorJob = Start-Process -FilePath "python" -ArgumentList "detector.py" -WindowStyle Normal -PassThru
Start-Sleep -Seconds 2

Write-Host "[3/3] Starting frontend server..." -ForegroundColor Yellow
$frontendJob = Start-Process -FilePath "python" -ArgumentList "-m", "http.server", "8000" -WindowStyle Normal -PassThru
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  All Services Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Frontend: " -NoNewline
Write-Host "http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Stream:   " -NoNewline
Write-Host "http://localhost:1919/stream" -ForegroundColor Cyan
Write-Host "  API:      " -NoNewline
Write-Host "http://localhost:1145" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Process IDs:" -ForegroundColor Gray
Write-Host "    Server:   $($serverJob.Id)" -ForegroundColor Gray
Write-Host "    Detector: $($detectorJob.Id)" -ForegroundColor Gray
Write-Host "    Frontend: $($frontendJob.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -NoNewline
Write-Host ""

@{
    Server = $serverJob.Id
    Detector = $detectorJob.Id
    Frontend = $frontendJob.Id
} | ConvertTo-Json | Out-File -FilePath ".pids.json" -Encoding UTF8

try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host ""
    Write-Host "[INFO] Stopping all services..." -ForegroundColor Yellow
    Stop-Process -Id $serverJob.Id -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $detectorJob.Id -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $frontendJob.Id -Force -ErrorAction SilentlyContinue
    Remove-Item ".pids.json" -ErrorAction SilentlyContinue
    Write-Host "[OK] All services stopped" -ForegroundColor Green
}
