#!/bin/bash
# Restart Splunk Docker container for Mac/Linux

echo "Restarting Splunk container..."
echo ""

# Stop the container
echo "Stopping container..."
if docker stop splunk >/dev/null 2>&1; then
    echo "✓ Container stopped"
else
    echo "⚠️  Container was not running"
fi

echo ""

# Start the container
echo "Starting container..."
if docker start splunk >/dev/null 2>&1; then
    echo "✓ Container started"
    echo ""
    echo "Access Splunk at: http://localhost:8000"
    echo "Username: admin"
    echo "Password: password"
    echo ""
    echo "Waiting for Splunk to be ready..."
    sleep 10
    echo "✓ Splunk should be ready now"
else
    echo "✗ Failed to start container"
    echo "Try running ./start-splunk.sh instead"
    exit 1
fi
