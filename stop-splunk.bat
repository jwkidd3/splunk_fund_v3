@echo off
echo Stopping Splunk container...

docker stop splunk
if %ERRORLEVEL% EQU 0 (
    echo Splunk container stopped successfully!
) else (
    echo Failed to stop Splunk container
)

echo Removing Splunk container...
docker rm splunk
if %ERRORLEVEL% EQU 0 (
    echo Splunk container removed successfully!
) else (
    echo Failed to remove Splunk container
)
