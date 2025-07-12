# Production Deployment Guide

This guide covers deploying FLEXT-Meltano in production environments with enterprise-grade reliability, security, and monitoring.

## 🎯 Production Requirements

### System Requirements

#### Minimum Requirements
- **CPU**: 4 cores (8+ recommended for high throughput)
- **Memory**: 8GB RAM (16GB+ recommended)
- **Storage**: 100GB SSD (varies by data volume)
- **Network**: 1Gbps+ for large data transfers

#### Software Requirements
- **Python**: 3.13+ with async/await support
- **Operating System**: Linux (Ubuntu 22.04 LTS recommended)
- **Database**: PostgreSQL 14+ for state management
- **Message Queue**: Redis 7+ for job queuing
- **Monitoring**: Prometheus + Grafana stack

### Architecture Overview

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[nginx/HAProxy]
    end
    
    subgraph "Application Layer"
        App1[FLEXT-Meltano Instance 1]
        App2[FLEXT-Meltano Instance 2]
        App3[FLEXT-Meltano Instance N]
    end
    
    subgraph "Data Layer"
        PostgreSQL[(PostgreSQL Cluster)]
        Redis[(Redis Cluster)]
        Storage[(Object Storage)]
    end
    
    subgraph "Monitoring"
        Prometheus[Prometheus]
        Grafana[Grafana]
        AlertManager[Alert Manager]
    end
    
    LB --> App1
    LB --> App2
    LB --> App3
    
    App1 --> PostgreSQL
    App1 --> Redis
    App1 --> Storage
    
    App2 --> PostgreSQL
    App2 --> Redis
    App2 --> Storage
    
    App3 --> PostgreSQL
    App3 --> Redis
    App3 --> Storage
    
    App1 --> Prometheus
    App2 --> Prometheus
    App3 --> Prometheus
    
    Prometheus --> Grafana
    Prometheus --> AlertManager
```

## 🚀 Installation and Setup

### 1. System Preparation

```bash
#!/bin/bash
# system_setup.sh

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    python3.13 \
    python3.13-venv \
    python3.13-dev \
    build-essential \
    git \
    curl \
    wget \
    postgresql-client \
    redis-tools \
    nginx

# Install Docker for containerized deployment
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. User and Directory Setup

```bash
#!/bin/bash
# user_setup.sh

# Create service user
sudo useradd -r -s /bin/bash -d /opt/flext-meltano flext-meltano

# Create directory structure
sudo mkdir -p /opt/flext-meltano/{app,data,logs,backups,config}
sudo mkdir -p /var/log/flext-meltano
sudo mkdir -p /etc/flext-meltano

# Set ownership
sudo chown -R flext-meltano:flext-meltano /opt/flext-meltano
sudo chown -R flext-meltano:flext-meltano /var/log/flext-meltano
sudo chown -R flext-meltano:flext-meltano /etc/flext-meltano
```

### 3. Application Deployment

#### Python Environment Setup

```bash
#!/bin/bash
# app_setup.sh

# Switch to service user
sudo -u flext-meltano bash << 'EOF'

cd /opt/flext-meltano/app

# Clone application
git clone https://github.com/your-org/flext-meltano.git .

# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -e .

# Install production dependencies
pip install gunicorn uvicorn[standard] prometheus-client

EOF
```

#### Configuration Files

**Production Environment Configuration**:
```bash
# /etc/flext-meltano/production.env

# Application Settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://flext_user:secure_password@db-cluster:5432/flext_meltano
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Redis Configuration
REDIS_URL=redis://redis-cluster:6379/0
REDIS_MAX_CONNECTIONS=100

# Meltano Configuration
MELTANO_PROJECT_ROOT=/opt/flext-meltano/data/projects
MELTANO_ENVIRONMENT=production
MELTANO_STATE_BACKEND=postgresql://flext_user:secure_password@db-cluster:5432/meltano_state

# Singer SDK Configuration (Zero Warnings)
SINGER_SDK_LOG_LEVEL=ERROR
SINGER_SDK_DISABLE_WARNINGS=true
PYTHONWARNINGS=ignore::DeprecationWarning,ignore::PendingDeprecationWarning

# Performance Settings
MELTANO_MAX_WORKERS=8
MELTANO_JOB_TIMEOUT=7200
MELTANO_MEMORY_LIMIT=8Gi
MELTANO_CACHE_TTL=3600

# Security Settings
SECRET_KEY=your-super-secure-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Monitoring
PROMETHEUS_METRICS_ENABLED=true
PROMETHEUS_METRICS_PORT=9090
OPENTELEMETRY_ENABLED=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://prometheus:4317

# Logging
LOG_FILE=/var/log/flext-meltano/app.log
LOG_ROTATION=daily
LOG_RETENTION_DAYS=30

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * *  # Daily at 2 AM
BACKUP_RETENTION_DAYS=90
BACKUP_STORAGE=s3://your-backup-bucket/flext-meltano

# External Integrations
ORACLE_OIC_ENDPOINT=https://your-oic-instance.oraclecloud.com
ORACLE_OIC_CLIENT_ID=your_client_id
ORACLE_OIC_CLIENT_SECRET=your_client_secret

LDAP_SERVER=ldaps://ldap.company.com:636
LDAP_BIND_DN=cn=service,dc=company,dc=com
LDAP_BIND_PASSWORD=service_password
```

## 🐳 Container Deployment

### Docker Compose Production Setup

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.production
    image: flext-meltano:latest
    replicas: 3
    environment:
      - ENV_FILE=/etc/flext-meltano/production.env
    volumes:
      - ./config:/etc/flext-meltano
      - ./data:/opt/flext-meltano/data
      - ./logs:/var/log/flext-meltano
    ports:
      - "8000-8002:8000"
    depends_on:
      - postgresql
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2"
        reservations:
          memory: 2G
          cpus: "1"

  postgresql:
    image: postgres:16
    environment:
      POSTGRES_DB: flext_meltano
      POSTGRES_USER: flext_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2"

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 1gb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin_password
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

### Production Dockerfile

```dockerfile
# Dockerfile.production
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -r -s /bin/bash -d /app flext-meltano

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install application
RUN pip install -e .

# Change ownership
RUN chown -R flext-meltano:flext-meltano /app

# Switch to app user
USER flext-meltano

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "src.flext_meltano.app:app"]
```

## ⚙️ Configuration Management

### Environment-Specific Configuration

```python
# config/production.py
import os
from pathlib import Path

class ProductionConfig:
    """Production environment configuration."""
    
    # Application
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_POOL_SIZE = int(os.getenv('DATABASE_POOL_SIZE', '20'))
    DATABASE_MAX_OVERFLOW = int(os.getenv('DATABASE_MAX_OVERFLOW', '30'))
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL')
    REDIS_MAX_CONNECTIONS = int(os.getenv('REDIS_MAX_CONNECTIONS', '100'))
    
    # Meltano
    MELTANO_PROJECT_ROOT = Path(os.getenv('MELTANO_PROJECT_ROOT', '/opt/flext-meltano/data/projects'))
    MELTANO_ENVIRONMENT = os.getenv('MELTANO_ENVIRONMENT', 'production')
    MELTANO_MAX_WORKERS = int(os.getenv('MELTANO_MAX_WORKERS', '8'))
    MELTANO_JOB_TIMEOUT = int(os.getenv('MELTANO_JOB_TIMEOUT', '7200'))
    
    # Monitoring
    PROMETHEUS_METRICS_ENABLED = os.getenv('PROMETHEUS_METRICS_ENABLED', 'true').lower() == 'true'
    OPENTELEMETRY_ENABLED = os.getenv('OPENTELEMETRY_ENABLED', 'true').lower() == 'true'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = Path(os.getenv('LOG_FILE', '/var/log/flext-meltano/app.log'))
    
    # Security
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        required_vars = [
            'SECRET_KEY',
            'DATABASE_URL',
            'REDIS_URL',
            'JWT_SECRET_KEY',
            'ENCRYPTION_KEY'
        ]
        
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
```

### Secrets Management

```bash
#!/bin/bash
# secrets_setup.sh

# Using HashiCorp Vault (recommended)
vault kv put secret/flext-meltano/production \
    secret_key="$(openssl rand -base64 32)" \
    jwt_secret_key="$(openssl rand -base64 32)" \
    encryption_key="$(openssl rand -base64 32)" \
    database_password="$(openssl rand -base64 24)" \
    oracle_client_secret="your_oracle_secret" \
    ldap_bind_password="your_ldap_password"

# Alternative: Using Kubernetes secrets
kubectl create secret generic flext-meltano-secrets \
    --from-literal=secret-key="$(openssl rand -base64 32)" \
    --from-literal=jwt-secret-key="$(openssl rand -base64 32)" \
    --from-literal=database-password="$(openssl rand -base64 24)"
```

## 🔐 Security Configuration

### SSL/TLS Setup

```nginx
# nginx.conf
upstream flext_meltano {
    server app:8000;
    server app:8001;
    server app:8002;
}

server {
    listen 80;
    server_name flext-meltano.company.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name flext-meltano.company.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;

    location / {
        proxy_pass http://flext_meltano;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /health {
        proxy_pass http://flext_meltano/health;
        access_log off;
    }

    location /metrics {
        proxy_pass http://flext_meltano/metrics;
        allow 10.0.0.0/8;  # Restrict to internal networks
        deny all;
    }
}
```

### Database Security

```sql
-- database_security.sql

-- Create dedicated user with limited privileges
CREATE USER flext_user WITH PASSWORD 'secure_password';

-- Create databases
CREATE DATABASE flext_meltano OWNER flext_user;
CREATE DATABASE meltano_state OWNER flext_user;

-- Grant necessary privileges
GRANT CONNECT ON DATABASE flext_meltano TO flext_user;
GRANT CONNECT ON DATABASE meltano_state TO flext_user;

-- Create schemas
\c flext_meltano
CREATE SCHEMA IF NOT EXISTS app AUTHORIZATION flext_user;
CREATE SCHEMA IF NOT EXISTS audit AUTHORIZATION flext_user;

\c meltano_state  
CREATE SCHEMA IF NOT EXISTS state AUTHORIZATION flext_user;

-- Enable row level security
ALTER TABLE app.sensitive_table ENABLE ROW LEVEL SECURITY;

-- Create security policies
CREATE POLICY user_data_policy ON app.user_data
    FOR ALL TO flext_user
    USING (tenant_id = current_setting('app.current_tenant_id'));
```

## 📊 Monitoring and Observability

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "flext_meltano_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'flext-meltano'
    static_configs:
      - targets: ['app:8000', 'app:8001', 'app:8002']
    metrics_path: /metrics
    scrape_interval: 30s

  - job_name: 'postgresql'
    static_configs:
      - targets: ['postgresql:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

### Application Metrics

```python
# monitoring.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import functools

# Metrics definitions
pipeline_executions_total = Counter(
    'flext_meltano_pipeline_executions_total',
    'Total pipeline executions',
    ['project', 'status', 'environment']
)

pipeline_duration_seconds = Histogram(
    'flext_meltano_pipeline_duration_seconds',
    'Pipeline execution duration',
    ['project', 'environment']
)

active_pipelines = Gauge(
    'flext_meltano_active_pipelines',
    'Number of currently active pipelines'
)

def monitor_pipeline_execution(func):
    """Decorator to monitor pipeline executions."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        project_name = kwargs.get('project_name', 'unknown')
        environment = kwargs.get('environment', 'unknown')
        
        start_time = time.time()
        active_pipelines.inc()
        
        try:
            result = await func(*args, **kwargs)
            status = 'success' if result.get('success') else 'failed'
            pipeline_executions_total.labels(
                project=project_name,
                status=status,
                environment=environment
            ).inc()
            return result
            
        except Exception as e:
            pipeline_executions_total.labels(
                project=project_name,
                status='error',
                environment=environment
            ).inc()
            raise
            
        finally:
            duration = time.time() - start_time
            pipeline_duration_seconds.labels(
                project=project_name,
                environment=environment
            ).observe(duration)
            active_pipelines.dec()
    
    return wrapper

# Start metrics server
def start_metrics_server(port=9090):
    start_http_server(port)
```

### Grafana Dashboards

```json
{
  "dashboard": {
    "title": "FLEXT-Meltano Production Dashboard",
    "panels": [
      {
        "title": "Pipeline Execution Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(flext_meltano_pipeline_executions_total[5m])",
            "legendFormat": "{{project}} - {{status}}"
          }
        ]
      },
      {
        "title": "Active Pipelines",
        "type": "singlestat",
        "targets": [
          {
            "expr": "flext_meltano_active_pipelines"
          }
        ]
      },
      {
        "title": "Pipeline Duration (95th percentile)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(flext_meltano_pipeline_duration_seconds_bucket[5m]))",
            "legendFormat": "{{project}}"
          }
        ]
      }
    ]
  }
}
```

## 🔄 Deployment Automation

### CI/CD Pipeline

```yaml
# .github/workflows/deploy-production.yml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=src/flext_meltano tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: |
          docker build -f Dockerfile.production -t flext-meltano:${{ github.ref_name }} .
          docker tag flext-meltano:${{ github.ref_name }} flext-meltano:latest
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push flext-meltano:${{ github.ref_name }}
          docker push flext-meltano:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          # Update production environment
          ssh ${{ secrets.PROD_SSH_HOST }} "
            cd /opt/flext-meltano/app &&
            docker-compose -f docker-compose.production.yml pull &&
            docker-compose -f docker-compose.production.yml up -d --remove-orphans
          "
      - name: Health check
        run: |
          sleep 30
          curl -f https://flext-meltano.company.com/health
```

### Blue-Green Deployment

```bash
#!/bin/bash
# blue_green_deploy.sh

CURRENT_COLOR=$(docker ps --format "table {{.Names}}" | grep flext-meltano | head -1 | cut -d'-' -f3)
NEW_COLOR=$([ "$CURRENT_COLOR" = "blue" ] && echo "green" || echo "blue")

echo "Current deployment: $CURRENT_COLOR"
echo "Deploying to: $NEW_COLOR"

# Deploy new version
docker-compose -f docker-compose.$NEW_COLOR.yml up -d

# Health check
echo "Performing health check..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health; then
        echo "Health check passed"
        break
    fi
    echo "Health check attempt $i failed, retrying..."
    sleep 10
done

# Switch traffic
echo "Switching traffic to $NEW_COLOR"
sed -i "s/upstream.*{/upstream flext_meltano {\n    server app-$NEW_COLOR:8000;/" /etc/nginx/nginx.conf
nginx -s reload

# Stop old deployment
echo "Stopping $CURRENT_COLOR deployment"
docker-compose -f docker-compose.$CURRENT_COLOR.yml down

echo "Deployment complete"
```

## 🔧 Maintenance and Operations

### Backup Strategy

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/flext-meltano/backups"

# Database backup
pg_dump -h postgresql -U flext_user flext_meltano > $BACKUP_DIR/db_backup_$DATE.sql
pg_dump -h postgresql -U flext_user meltano_state > $BACKUP_DIR/state_backup_$DATE.sql

# Application data backup
tar -czf $BACKUP_DIR/data_backup_$DATE.tar.gz /opt/flext-meltano/data

# Upload to S3
aws s3 cp $BACKUP_DIR/db_backup_$DATE.sql s3://flext-backups/production/
aws s3 cp $BACKUP_DIR/state_backup_$DATE.sql s3://flext-backups/production/
aws s3 cp $BACKUP_DIR/data_backup_$DATE.tar.gz s3://flext-backups/production/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### Log Management

```bash
#!/bin/bash
# log_rotation.sh

# Configure logrotate
cat > /etc/logrotate.d/flext-meltano << EOF
/var/log/flext-meltano/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
    postrotate
        systemctl reload flext-meltano
    endscript
}
EOF
```

---

**Next Steps**: 
- [Configuration Guide](./configuration.md) for detailed configuration options
- [Monitoring Guide](./monitoring.md) for comprehensive monitoring setup
- [Troubleshooting](./troubleshooting.md) for common issues and solutions