# Splunk Fundamentals - Mac/Linux Scripts

This folder contains shell scripts for managing Splunk on Mac/Linux environments using Docker.

## Prerequisites

- Docker Desktop for Mac installed and running
- Terminal access
- Internet connection (for first-time setup)

## Scripts Overview

| Script | Purpose | Usage |
|--------|---------|-------|
| `start-splunk.sh` | Start or create Splunk container | `./start-splunk.sh` |
| `stop-splunk.sh` | Stop the Splunk container | `./stop-splunk.sh` |
| `restart-splunk.sh` | Restart the Splunk container | `./restart-splunk.sh` |
| `status-splunk.sh` | Check container status | `./status-splunk.sh` |
| `cleanup-splunk.sh` | Remove container and image | `./cleanup-splunk.sh` |
| `update-course.sh` | Update course materials from git | `./update-course.sh` |

## First-Time Setup

1. **Make scripts executable:**
   ```bash
   chmod +x *.sh
   ```

2. **Start Splunk:**
   ```bash
   ./start-splunk.sh
   ```

3. **Wait for initialization** (2-3 minutes on first run)

4. **Access Splunk:**
   - URL: http://localhost:8000
   - Username: `admin`
   - Password: `password`

## Common Tasks

### Start Splunk
```bash
./start-splunk.sh
```
Creates a new container if needed, or starts the existing one.

### Check Status
```bash
./status-splunk.sh
```
Shows whether Splunk is running, stopped, or not created.

### Stop Splunk
```bash
./stop-splunk.sh
```
Stops the container but preserves data.

### Restart Splunk
```bash
./restart-splunk.sh
```
Stops and starts the container.

### Update Course Materials
```bash
./update-course.sh
```
Pulls latest changes from the git repository.

### Complete Cleanup
```bash
./cleanup-splunk.sh
```
⚠️ **Warning:** Removes container, image, and all data. Use only when you want a fresh start.

## Troubleshooting

### Script Permission Denied
```bash
chmod +x scripts/mac/*.sh
```

### Docker Not Running
Start Docker Desktop before running these scripts.

### Port 8000 Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process or change Splunk port in start-splunk.sh
```

### Container Won't Start
```bash
# Check Docker logs
docker logs splunk

# Try complete cleanup and restart
./cleanup-splunk.sh
./start-splunk.sh
```

### Splunk Taking Too Long to Start
First startup can take 2-3 minutes. Monitor progress:
```bash
docker logs -f splunk
```
Press Ctrl+C to exit log view.

## Container Details

- **Container Name:** `splunk`
- **Port:** 8000
- **Platform:** linux/amd64 (required for Mac M1/M2)
- **Image:** splunk/splunk:latest
- **Default Credentials:**
  - Username: `admin`
  - Password: `password`

## Useful Docker Commands

```bash
# View container logs
docker logs -f splunk

# Execute commands inside container
docker exec -it splunk bash

# View container resource usage
docker stats splunk

# Remove container only (keep image)
docker rm -f splunk

# List all containers
docker ps -a

# List all images
docker images
```

## Notes

- Data persists between container stops/starts
- Data is lost when container is removed (`docker rm`)
- Use `cleanup-splunk.sh` for complete removal
- Scripts auto-detect course directory location
- All scripts include user-friendly output with status indicators (✓, ✗, ⚠️)

## Support

For issues specific to:
- **Scripts:** Check this README or script comments
- **Docker:** See Docker Desktop documentation
- **Splunk:** See course labs or Splunk documentation

## See Also

- [Splunk Docker Documentation](https://splunk.github.io/docker-splunk/)
- [Docker Desktop for Mac](https://docs.docker.com/desktop/mac/install/)
- Main course README: `../../README.md`
