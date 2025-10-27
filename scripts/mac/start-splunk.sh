#!/bin/bash
# Start Splunk Docker container for Mac/Linux
# This script will start an existing container or create a new one if needed

echo "Starting Splunk container..."

# Try to start existing container
if docker start splunk >/dev/null 2>&1; then
    echo "✓ Splunk container started successfully!"
    echo ""
    echo "Access Splunk at: http://localhost:8000"
    echo "Username: admin"
    echo "Password: password"
    echo ""
    echo "Waiting for Splunk to be ready (this may take 1-2 minutes)..."
    sleep 10
else
    echo "Container does not exist, creating new one..."
    echo ""

    # Create and start new container
    docker run -d \
        -p 8000:8000 \
        -e SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com \
        -e SPLUNK_START_ARGS=--accept-license \
        --platform linux/amd64 \
        -e "SPLUNK_PASSWORD=password" \
        --name splunk \
        splunk/splunk:latest

    if [ $? -eq 0 ]; then
        echo "✓ Splunk container created and started successfully!"
        echo ""
        echo "Access Splunk at: http://localhost:8000"
        echo "Username: admin"
        echo "Password: password"
        echo ""
        echo "Note: First startup may take 2-3 minutes while Splunk initializes..."
        echo "You can check status with: docker logs -f splunk"
    else
        echo "✗ Failed to create Splunk container"
        echo "Make sure Docker is running and you have internet connectivity"
        exit 1
    fi
fi
