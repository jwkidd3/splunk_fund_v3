@echo off
echo Starting Splunk container...

docker run -d ^
  -p 8000:8000 ^
  -e SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com ^
  -e SPLUNK_START_ARGS=--accept-license ^
  --platform linux/amd64 ^
  -e "SPLUNK_PASSWORD=password" ^
  --name splunk ^
  splunk/splunk:latest

if %ERRORLEVEL% EQU 0 (
    echo Splunk container started successfully!
    echo Access Splunk at: http://localhost:8000
    echo Username: admin
    echo Password: password
) else (
    echo Failed to start Splunk container
)
