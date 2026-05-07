# Lab 2: Docker Setup Checklist

## Prerequisites Status
- ❌ Docker Daemon: Not currently running
  - Solution: Start Docker Desktop or Docker Service
  - On Windows: Open Docker Desktop application
  - On Linux: Run `sudo systemctl start docker`

- ❌ Docker Compose: Need verification after Docker starts

## Setup Instructions for Docker

### Step 1: Install Docker Desktop (Windows)
1. Download from: https://www.docker.com/products/docker-desktop
2. Install Docker Desktop
3. Start Docker Desktop (appears in system tray)
4. Wait for "Docker Engine running" indicator

### Step 2: Verify Installation
```bash
docker --version
docker-compose --version
```

### Step 3: Build and Run Containers
```bash
cd d:\python\Bas prog fwd
docker-compose build
docker-compose up -d
```

### Step 4: Verify Setup
```bash
# List running containers
docker ps

# Check PostgreSQL logs
docker logs fastapi_postgres

# Check FastAPI logs
docker logs fastapi_app

# Test API endpoint
curl http://localhost:8000/health
```

### Step 5: View Container Libraries
```bash
# List installed Python packages
docker-compose exec fastapi pip list

# Show more detailed package info
docker-compose exec fastapi poetry show
```

## Project Configuration

### Dockerfile Features
✅ Based on Python 3.11-slim
✅ Installs system dependencies (gcc, postgresql-client)
✅ Uses Poetry for dependency management
✅ Auto-reload enabled via Uvicorn reload flag
✅ Health check configured
✅ Volume mounting defined in docker-compose

### Docker Compose Features
✅ PostgreSQL 15 (Alpine Linux) - lightweight
✅ FastAPI application with auto-reload
✅ Volume mounts for live code updates
✅ Health checks for both services
✅ Network bridge for inter-container communication
✅ Environment variables configured
✅ Database persistence with named volumes

## Expected Results After Running Containers

### Containers Running
```
CONTAINER ID   IMAGE                    STATUS
abc123...      fastapi_postgres:latest  Up (healthy)
def456...      fastapi_app:latest       Up (healthy)
```

### API Access Points
- FastAPI API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health
- PostgreSQL: localhost:5432

### Database Connection
- Host: postgres (from within containers)
- Host: localhost (from host machine)
- Port: 5432
- Database: fastapi_db
- User: postgres
- Password: password

## Troubleshooting

### Docker Daemon Not Running
**Error**: "Cannot connect to Docker daemon"
**Solution**:
1. Open Docker Desktop application
2. Wait for initialization (30-60 seconds)
3. Check system tray for Docker icon
4. Retry docker-compose command

### Ports Already in Use
**Error**: "bind: address already in use"
**Solution**:
```bash
# Find process using port
netstat -ano | findstr :8000
netstat -ano | findstr :5432

# Update docker-compose.yml ports section if needed:
# ports:
#   - "8001:8000"  # Use different host port
```

### Container Exit/Crash
**Check logs**:
```bash
docker-compose logs fastapi_app
docker-compose logs fastapi_postgres
```

### Database Connection Refused
**Solution**:
```bash
# Ensure PostgreSQL is healthy
docker-compose exec postgres pg_isready -U postgres

# Check database URL in .env
cat .env
```

## Manual Testing Steps

### Test 1: Container Health
```bash
docker ps
# Should show both containers with "Up" status
```

### Test 2: API Response
```bash
# Windows PowerShell
Invoke-WebRequest http://localhost:8000/health

# Or use curl if installed
curl http://localhost:8000/health
```

### Test 3: Database Connection
```bash
docker-compose exec postgres psql -U postgres -d fastapi_db -c "SELECT NOW();"
```

### Test 4: Hot Reload
1. Access FastAPI Swagger UI: http://localhost:8000/docs
2. Modify `app/main.py` locally
3. Refresh browser - changes should appear immediately

## Next Steps

After successful Docker setup:
1. Record screenshots of running containers
2. Document any custom configurations
3. Test all API endpoints
4. Verify database connectivity
5. Confirm auto-reload functionality
6. Ready for Lab 3: User CRUD operations
