#!/bin/bash
# Update course materials from git repository for Mac/Linux

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Course root is two levels up from scripts/mac
COURSE_DIR="$( cd "$SCRIPT_DIR/../.." && pwd )"

echo "📚 Updating Splunk Fundamentals Course Materials"
echo "================================================"
echo ""
echo "Course directory: $COURSE_DIR"
echo ""

# Change to course directory
cd "$COURSE_DIR" || exit 1

# Check if this is a git repository
if [ ! -d ".git" ]; then
    echo "✗ This directory is not a git repository"
    echo "Cannot update course materials automatically"
    exit 1
fi

echo "Pulling latest changes from repository..."
echo ""

# Pull latest changes
if git pull; then
    echo ""
    echo "✓ Course materials updated successfully!"
    echo ""
    echo "Changes applied:"
    git log -1 --pretty=format:"  Commit: %h%n  Author: %an%n  Date: %ar%n  Message: %s%n"
else
    echo ""
    echo "✗ Failed to update course materials"
    echo "You may need to resolve conflicts manually"
    exit 1
fi
