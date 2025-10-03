@echo off
powershell -Command "Set-Location C:\Users\Administrator\splunk_fund_v3; Write-Host 'Pulling latest changes from repository...' -ForegroundColor Green; git pull; Write-Host 'Pull complete!' -ForegroundColor Green"
pause
