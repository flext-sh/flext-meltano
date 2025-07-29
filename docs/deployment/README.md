# FLEXT Meltano Deployment Guide

Enterprise deployment patterns and production considerations for FLEXT Meltano.

## 🚀 Deployment Overview

FLEXT Meltano is designed as a **library component** within the larger FLEXT ecosystem, primarily consumed by Go services via bridge pattern integration.

### Deployment Architecture

```
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   FlexCore      │    │   FLEXT Service     │    │   FLEXT Meltano     │
│   (Go Service)  │◄──►│   (Go/Python)       │◄──►│   (Python Library)  │
│   Port 8080     │    │   Port 8081         │    │   Subprocess Exec   │
└─────────────────┘    └─────────────────────┘    └─────────────────────┘
         │                        │                         │
         ▼                        ▼                         ▼
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   PostgreSQL    │    │      Redis          │    │     Meltano         │
│   Port 5433     │    │   Port 6380         │    │   CLI + Plugins     │
└─────────────────┘    └─────────────────────┘    └─────────────────────┘
```

## 🐳 Docker Deployment

### Container Strategy

FLEXT Meltano is packaged as part of the FLEXT service container, not as a standalone service.

#### Base Dockerfile Pattern

```dockerfile
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY src/ ./src/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-dev

# Set environment variables
ENV PYTHONPATH=/app/src:$PYTHONPATH
ENV MELTANO_PROJECT_ROOT=/app
ENV MELTANO_ENVIRONMENT=production

# Copy bridge scripts
COPY scripts/ ./scripts/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import flext_meltano; print('OK')" || exit 1

# Entry point for bridge operations
ENTRYPOINT ["python", "scripts/flext_meltano_bridge.py"]
```

### Multi-stage Build

```dockerfile
# Build stage
FROM python:3.13-slim as builder

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only=main

# Production stage
FROM python:3.13-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY src/ ./src/
COPY scripts/ ./scripts/

ENV PYTHONPATH=/app/src:$PYTHONPATH
CMD ["python", "scripts/flext_meltano_bridge.py", "--help"]
```

## ⚙️ Configuration Management

### Environment Variables

#### Required Variables

```bash
# Core configuration
MELTANO_PROJECT_ROOT=/app
MELTANO_ENVIRONMENT=production
PYTHONPATH=/app/src:$PYTHONPATH

# Database (if using Meltano system database)
MELTANO_DATABASE_URI=postgresql://user:pass@postgres:5432/meltano

# Optional configuration
MELTANO_UI_BIND_PORT=5000
SINGER_SDK_LOG_LEVEL=INFO
FLEXT_MELTANO_AUTO_INSTALL=true
FLEXT_MELTANO_STATE_BACKEND=filesystem
```

#### Go Service Integration

```bash
# FLEXT service configuration for bridge integration
FLEXT_MELTANO_BRIDGE_SCRIPT=/app/scripts/flext_meltano_bridge.py
FLEXT_MELTANO_PYTHON_PATH=/usr/local/bin/python
FLEXT_MELTANO_TIMEOUT=300
```

### Configuration Files

#### Meltano Configuration

The library initializes Meltano projects on demand. For production, consider pre-initializing:

```yaml
# meltano.yml (example)
version: 1
default_environment: prod
project_id: "flext-meltano-prod"

environments:
  - name: prod
    config:
      plugins:
        extractors:
          - name: tap-csv
          - name: tap-postgres
        loaders:
          - name: target-csv
          - name: target-postgres
```

#### Production Configuration Template

```bash
# production.env
MELTANO_ENVIRONMENT=prod
MELTANO_PROJECT_ROOT=/app/meltano
MELTANO_DATABASE_URI=postgresql://meltano:${MELTANO_DB_PASSWORD}@postgres:5432/meltano_prod

# Singer settings
SINGER_SDK_LOG_LEVEL=WARNING
SINGER_SDK_BATCH_CONFIG={"encoding":{"format":"jsonl"}}

# FLEXT settings
FLEXT_MELTANO_AUTO_INSTALL=false
FLEXT_MELTANO_STATE_BACKEND=database
```

## 🔐 Security Considerations

### Production Security

#### Environment Secrets

```bash
# Use secret management for sensitive data
DATABASE_PASSWORD_FILE=/run/secrets/db_password
API_KEY_FILE=/run/secrets/api_key

# Or environment variables with rotation
DATABASE_PASSWORD=${VAULT_DATABASE_PASSWORD}
API_KEY=${VAULT_API_KEY}
```

#### Container Security

```dockerfile
# Run as non-root user
RUN adduser --disabled-password --gecos '' meltano
USER meltano

# Minimize attack surface
RUN apt-get remove -y build-essential curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Set secure file permissions
COPY --chown=meltano:meltano src/ ./src/
COPY --chown=meltano:meltano scripts/ ./scripts/
```

#### Network Security

- Isolate Meltano execution in dedicated network
- Use service mesh for inter-service communication
- Implement proper firewall rules
- Enable TLS for all external connections

### Audit & Compliance

```python
# Enable audit logging
import logging

audit_logger = logging.getLogger('flext_meltano.audit')
audit_logger.setLevel(logging.INFO)

# Log all bridge operations
def audit_bridge_operation(operation: str, args: list):
    audit_logger.info(f"Bridge operation: {operation}, args: {args}")
```

## 📊 Monitoring & Observability

### Health Checks

#### Bridge Health Check

```python
#!/usr/bin/env python3
"""Health check script for FLEXT Meltano."""

import sys
from flext_meltano.flext_meltano_execution import flext_meltano_run_command

def health_check():
    """Perform health check."""
    try:
        # Test basic functionality
        result = flext_meltano_run_command(["--version"])
        if result.success and "meltano" in result.output.lower():
            print("HEALTHY")
            return 0
        else:
            print("UNHEALTHY: Meltano not responding")
            return 1
    except Exception as e:
        print(f"UNHEALTHY: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(health_check())
```

#### Docker Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python /app/health_check.py || exit 1
```

### Metrics Collection

```python
# Integration with FLEXT observability
from flext_observability import metrics

# Track bridge operations
bridge_operations = metrics.Counter('flext_meltano_bridge_operations_total')
bridge_duration = metrics.Histogram('flext_meltano_bridge_duration_seconds')

# Track pipeline executions
pipeline_executions = metrics.Counter('flext_meltano_pipeline_executions_total')
pipeline_success_rate = metrics.Gauge('flext_meltano_pipeline_success_rate')
```

### Logging Configuration

```python
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'flext_meltano': {
            'level': 'INFO',
            'handlers': ['default'],
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

## 🚀 Production Deployment Patterns

### Kubernetes Deployment

#### Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flext-service
  labels:
    app: flext-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flext-service
  template:
    metadata:
      labels:
        app: flext-service
    spec:
      containers:
      - name: flext-service
        image: flext/flext-service:2.0.0
        ports:
        - containerPort: 8081
        env:
        - name: MELTANO_ENVIRONMENT
          value: "prod"
        - name: PYTHONPATH
          value: "/app/src"
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: password
        volumeMounts:
        - name: meltano-state
          mountPath: /app/.meltano
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "2000m"
            memory: "4Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8081
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8081
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: meltano-state
        persistentVolumeClaim:
          claimName: meltano-state-pvc
```

#### Service Manifest

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flext-service
spec:
  selector:
    app: flext-service
  ports:
  - protocol: TCP
    port: 8081
    targetPort: 8081
  type: ClusterIP
```

### Docker Compose Production

```yaml
version: '3.8'

services:
  flext-service:
    image: flext/flext-service:2.0.0
    ports:
      - "8081:8081"
    environment:
      - MELTANO_ENVIRONMENT=prod
      - MELTANO_DATABASE_URI=postgresql://meltano:${MELTANO_DB_PASSWORD}@postgres:5432/meltano_prod
      - PYTHONPATH=/app/src
    volumes:
      - meltano_state:/app/.meltano
      - meltano_logs:/app/logs
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: meltano_prod
      POSTGRES_USER: meltano
      POSTGRES_PASSWORD: ${MELTANO_DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"
    volumes:
      - redis_data:/data

volumes:
  meltano_state:
  meltano_logs:
  postgres_data:
  redis_data:
```

## 🔄 CI/CD Integration

### Build Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy FLEXT Meltano

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'
    
    - name: Install Poetry
      run: pip install poetry
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run quality gates
      run: |
        make validate
    
    - name: Test bridge integration
      run: |
        python scripts/flext_meltano_bridge.py version

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t flext/flext-service:${{ github.sha }} .
        docker tag flext/flext-service:${{ github.sha }} flext/flext-service:latest
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push flext/flext-service:${{ github.sha }}
        docker push flext/flext-service:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to production
      run: |
        # Deployment commands
        kubectl set image deployment/flext-service flext-service=flext/flext-service:${{ github.sha }}
```

## 🚨 Troubleshooting Production Issues

### Common Production Issues

#### Bridge Communication Failures

```bash
# Check bridge script
python scripts/flext_meltano_bridge.py version

# Check Python path
echo $PYTHONPATH

# Check Meltano installation
which meltano
meltano --version
```

#### Memory Issues

```bash
# Monitor memory usage
ps aux | grep python
docker stats flext-service

# Check for memory leaks
python -m memory_profiler your_script.py
```

#### Performance Issues

```bash
# Profile bridge operations
python -m cProfile scripts/flext_meltano_bridge.py version

# Monitor system resources
htop
iostat -x 1
```

### Production Monitoring

```bash
# Health check endpoint
curl http://localhost:8081/health

# Bridge operation monitoring
curl http://localhost:8081/metrics | grep flext_meltano

# Log analysis
kubectl logs -f deployment/flext-service
docker logs -f flext-service
```

## 📋 Production Checklist

### Pre-deployment

- [ ] All quality gates pass (`make validate`)
- [ ] Security scan completed
- [ ] Configuration reviewed and secrets secured
- [ ] Health checks implemented
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Rollback plan prepared

### Post-deployment

- [ ] Health checks passing
- [ ] Metrics being collected
- [ ] Logs properly formatted
- [ ] Bridge integration functional
- [ ] Performance within acceptable limits
- [ ] Security monitoring active

---

*Deployment Guide - Version 2.0.0-enterprise*
*Last Updated: 2025-01-29*