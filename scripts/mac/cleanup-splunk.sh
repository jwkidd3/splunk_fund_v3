#!/bin/bash
# Cleanup Splunk Docker container and image for Mac/Linux
# WARNING: This will remove all Splunk data and the container

echo "⚠️  WARNING: This will completely remove Splunk container and all data!"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "Removing Splunk container..."
if docker rm -f splunk >/dev/null 2>&1; then
    echo "✓ Splunk container removed"
else
    echo "⚠️  Container not found or already removed"
fi

echo ""
echo "Removing Splunk image..."
if docker rmi splunk/splunk:latest >/dev/null 2>&1; then
    echo "✓ Splunk image removed"
else
    echo "⚠️  Image not found or already removed"
fi

echo ""
echo "✓ Cleanup complete!"
echo "Run ./start-splunk.sh to create a fresh Splunk instance"
