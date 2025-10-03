@echo off
echo Removing Splunk container...

docker rm -f splunk
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
