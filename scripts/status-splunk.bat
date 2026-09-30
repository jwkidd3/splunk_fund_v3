@echo off
REM Check Splunk Docker container status for Windows

echo Splunk Container Status
echo =======================
echo.

docker ps -a --format "{{.Names}}" | findstr /B /C:"splunk" >nul 2>&1
if errorlevel 1 (
    echo Status: Not created
    echo.
    echo No Splunk container found.
    echo To create and start: start-splunk.bat
    goto :eof
)

for /f "delims=" %%S in ('docker inspect -f "{{.State.Status}}" splunk 2^>nul') do set STATUS=%%S

if "%STATUS%"=="running" (
    echo Status: Running
    echo.
    echo Container Details:
    docker ps --filter name=splunk --format "  ID: {{.ID}}  Image: {{.Image}}  Ports: {{.Ports}}"
    echo.
    echo Access Splunk at: http://localhost:8000
    echo Username: admin
    echo Password: password
    echo.
    echo To view logs: docker logs -f splunk
) else if "%STATUS%"=="exited" (
    echo Status: Stopped
    echo.
    echo To start: start-splunk.bat
) else (
    echo Status: %STATUS%
)
