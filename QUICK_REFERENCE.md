# Quick Commands Reference

## Git Commands

```bash
# Clone repository
git clone https://github.com/quater12/Fwd-programing.git
cd Fwd-programing

# Switch branches
git checkout dev          # Development branch with latest features
git checkout main         # Main/production branch
git checkout prod         # Production branch

# View branch history
git log --oneline
git log --graph --all --decorate

# Add and commit changes
git add .
git commit -m "Your message here"

# Push to GitHub
git push origin dev
git push origin main
```

## Docker Commands

```bash
# Build Docker images
docker-compose build

# Start containers in background
docker-compose up -d

# View running containers
docker ps

# View container logs
docker logs fastapi_app
docker logs fastapi_postgres

# Stop containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Execute command in container
docker-compose exec fastapi bash          # FastAPI shell
docker-compose exec postgres psql -U postgres  # PostgreSQL shell

# View installed packages
docker-compose exec fastapi pip list
docker-compose exec fastapi poetry show
```

## Poetry Commands (Local Development)

```bash
# Install dependencies
poetry install

# Add new package
poetry add package-name

# Activate virtual environment
poetry shell

# Run application
poetry run uvicorn app.main:app --reload

# Run tests
poetry run pytest
```

## FastAPI Access Points

```
Swagger UI (Interactive Docs): http://localhost:8000/docs
ReDoc (API Documentation): http://localhost:8000/redoc
Health Check: http://localhost:8000/health
Root Endpoint: http://localhost:8000
```

## Database Connection

```bash
# From host machine
psql -h localhost -U postgres -d fastapi_db

# From within PostgreSQL container
docker-compose exec postgres psql -U postgres -d fastapi_db

# Run a query
SELECT VERSION();
```

## VS Code Useful Extensions

- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Docker (ms-azuretools.vscode-docker)
- Thunder Client (rangav.vscode-thunder-client) - Alternative to Postman
- SQLTools (mtxr.sqltools) - Database Explorer
- REST Client (humao.rest-client) - For HTTP requests

## Common Troubleshooting

```bash
# Docker daemon not running
# Solution: Open Docker Desktop application

# Port already in use
netstat -ano | findstr :8000
netstat -ano | findstr :5432

# Clear Docker cache and rebuild
docker system prune -a
docker-compose build --no-cache

# Reset database
docker-compose down -v
docker-compose up -d
```

## File Structure Quick Reference

```
key files:
- app/main.py           # FastAPI app entry point
- app/core/config.py    # Configuration settings
- Dockerfile            # Docker image definition
- docker-compose.yml    # Multi-container setup
- pyproject.toml        # Poetry dependencies
- .env                  # Environment variables
- .gitignore           # Git ignore patterns
```

## Important Reminders

✅ Always work on `dev` branch for new features
✅ `main` branch should contain production-ready code
✅ Start Docker Desktop before running docker-compose commands
✅ Use `.env` file for sensitive data - never commit to git
✅ Commit regularly with meaningful messages
✅ Test locally before pushing to GitHub
✅ Check git status before committing
