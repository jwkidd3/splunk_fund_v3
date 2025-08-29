# GitHub Pull Script for Windows PowerShell
# Save as pull-updates.ps1

param(
    [string]$RepoPath = "C:\Users\Administrator\Desktop\splunk_fund_v3"
)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "   GitHub Repository Updater" -ForegroundColor Cyan  
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Change to repository directory
if (Test-Path $RepoPath) {
    Set-Location $RepoPath
    Write-Host "Repository path: $RepoPath" -ForegroundColor Green
} else {
    Write-Host "Error: Repository path not found: $RepoPath" -ForegroundColor Red
    Write-Host "Please update the RepoPath parameter" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if it's a git repository
if (-not (Test-Path ".git")) {
    Write-Host "Error: Not a git repository!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    # Show current branch
    Write-Host "Current branch:" -ForegroundColor Yellow
    $currentBranch = git branch --show-current
    Write-Host $currentBranch -ForegroundColor White
    Write-Host ""

    # Fetch latest changes
    Write-Host "Fetching latest changes..." -ForegroundColor Yellow
    git fetch origin
    
    # Check status
    Write-Host ""
    Write-Host "Repository status:" -ForegroundColor Yellow
    git status -s
    
    # Pull latest changes
    Write-Host ""
    Write-Host "Pulling latest changes..." -ForegroundColor Yellow
    $pullResult = git pull origin 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Repository updated successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Recent commits:" -ForegroundColor Yellow
        git log --oneline -5
    } else {
        Write-Host ""
        Write-Host "✗ Error occurred while updating:" -ForegroundColor Red
        Write-Host $pullResult -ForegroundColor Red
    }
    
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"