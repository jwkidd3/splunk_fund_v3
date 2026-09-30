@echo off
REM Restart the Splunk Docker container for Windows

echo Restarting Splunk container...
docker restart splunk
if errorlevel 1 (
    echo.
    echo Could not restart. Is the container created?
    echo To create and start: start-splunk.bat
    goto :eof
)

echo.
echo Splunk container restarted.
echo Splunk takes about a minute to become available.
echo Access Splunk at: http://localhost:8000
