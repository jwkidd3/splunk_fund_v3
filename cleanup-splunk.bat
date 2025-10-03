@echo off
echo Stopping Splunk container...

docker stop splunk
if %ERRORLEVEL% EQU 0 (
    echo Splunk container stopped successfully!
) else (
    echo Failed to stop Splunk container or container not running
)

echo Removing Splunk container...
docker rm splunk
if %ERRORLEVEL% EQU 0 (
    echo Splunk container removed successfully!
) else (
    echo Failed to remove Splunk container or container does not exist
)

echo Removing Splunk image...
docker rmi splunk/splunk:latest
if %ERRORLEVEL% EQU 0 (
    echo Splunk image removed successfully!
) else (
    echo Failed to remove Splunk image
)

echo Cleanup complete!
