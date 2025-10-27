#!/bin/bash
# Stop Splunk Docker container for Mac/Linux

echo "Stopping Splunk container..."

if docker stop splunk >/dev/null 2>&1; then
    echo "✓ Splunk container stopped successfully!"
else
    echo "✗ Failed to stop container (it may not be running)"
    exit 1
fi
