#!/bin/bash
# Check Splunk Docker container status for Mac/Linux

echo "Splunk Container Status"
echo "======================="
echo ""

# Check if container exists
if docker ps -a --format '{{.Names}}' | grep -q '^splunk$'; then
    # Get container status
    STATUS=$(docker inspect -f '{{.State.Status}}' splunk 2>/dev/null)

    case $STATUS in
        running)
            echo "Status: ✓ Running"
            echo ""
            echo "Container Details:"
            docker ps --filter name=splunk --format "  ID: {{.ID}}\n  Image: {{.Image}}\n  Created: {{.CreatedAt}}\n  Ports: {{.Ports}}"
            echo ""
            echo "Access Splunk at: http://localhost:8000"
            echo "Username: admin"
            echo "Password: password"
            echo ""
            echo "To view logs: docker logs -f splunk"
            ;;
        exited)
            echo "Status: ⚠️  Stopped"
            echo ""
            echo "To start: ./start-splunk.sh"
            ;;
        *)
            echo "Status: ⚠️  $STATUS"
            ;;
    esac
else
    echo "Status: ✗ Not created"
    echo ""
    echo "No Splunk container found."
    echo "To create and start: ./start-splunk.sh"
fi
