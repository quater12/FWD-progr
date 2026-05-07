# Lab 2: Docker Container Setup

## Objectives
- Set up two Docker containers: FastAPI application and PostgreSQL database
- Configure auto-reload for development
- Mount working directory for live code updates
- Document the complete setup process

## Prerequisites
- Docker installed and running
- Docker Compose installed
- Python 3.11+
- Poetry installed

## Command Sequence for Lab 2

### 1. Build and Start Containers
```bash
# Navigate to project directory
cd d:\python\Bas prog fwd

# Build and start containers with docker-compose
docker-compose up -d

# Check if containers are running
docker ps
```

### 2. Verify Database Connection
```bash
# Check PostgreSQL container logs
docker logs fastapi_postgres

# Test database connection
docker-compose exec postgres pg_isready -U postgres
```

### 3. Verify FastAPI Application
```bash
# Check FastAPI container logs
docker logs fastapi_app

# Test FastAPI health endpoint
curl http://localhost:8000/health

# Access API documentation
# Open browser: http://localhost:8000/docs
```

### 4. View Installed Libraries in Container
```bash
# List all installed packages
docker-compose exec fastapi pip list

# Show Poetry dependencies
docker-compose exec fastapi poetry show
```

### 5. Execute Commands Inside Container
```bash
# Access FastAPI container shell
docker-compose exec fastapi bash

# Inside container, check Python version
python --version

# Inside container, check installed packages
pip list
```

### 6. Stop and Remove Containers
```bash
# Stop containers
docker-compose down

# Stop containers and remove volumes
docker-compose down -v
```

## Configuration Details

### Environment Variables (.env file)
- POSTGRES_USER: postgres
- POSTGRES_PASSWORD: password
- POSTGRES_DB: fastapi_db
- DATABASE_URL: postgresql+asyncpg://postgres:password@postgres:5432/fastapi_db

### Volume Mounts
- FastAPI source code mounted to enable hot-reload
- PostgreSQL data persisted in named volume `postgres_data`

### Ports
- FastAPI: 8000 (host) -> 8000 (container)
- PostgreSQL: 5432 (host) -> 5432 (container)

## Troubleshooting

### Connection Refused
```bash
# Wait for PostgreSQL to be ready
docker-compose exec postgres pg_isready -U postgres

# Check container health
docker inspect --format='{{.State.Health.Status}}' fastapi_postgres
```

### Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Change port in docker-compose.yml if needed
# ports:
#   - "8001:8000"
```

### Rebuild Containers
```bash
# Remove old containers and rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Verification Checklist
- [ ] Docker containers are running
- [ ] PostgreSQL is healthy and accessible
- [ ] FastAPI application starts without errors
- [ ] API health endpoint responds correctly
- [ ] Code changes reflect immediately (auto-reload working)
- [ ] Database connection established
- [ ] All required libraries installed in container
