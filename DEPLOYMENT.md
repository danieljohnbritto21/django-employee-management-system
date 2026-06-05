# Employee Management System - Deployment Guide

## Development vs Production

### Development Settings
- DEBUG = True
- ALLOWED_HOSTS = []
- SQLite3 database
- No HTTPS required

### Production Settings
- DEBUG = False
- ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
- PostgreSQL or MySQL database
- HTTPS required
- Environment variables for secrets

## Pre-Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Generate new SECRET_KEY
- [ ] Update ALLOWED_HOSTS
- [ ] Configure database (PostgreSQL/MySQL)
- [ ] Set up static files directory
- [ ] Configure media files directory
- [ ] Enable HTTPS/SSL
- [ ] Set up environment variables
- [ ] Run security checks
- [ ] Create backups
- [ ] Set up logging
- [ ] Configure email backend

## Step 1: Update settings.py for Production

```python
# settings.py

DEBUG = False

# Change to your actual domain
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', '127.0.0.1']

# Generate new secret key:
# from django.core.management.utils import get_random_secret_key
# print(get_random_secret_key())
SECRET_KEY = 'your-new-secret-key-here'

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}

# Database Configuration (PostgreSQL Example)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'employee_db',
        'USER': 'db_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/employee_management/static/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/employee_management/media/'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-email-password'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/employee_management/django.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

## Step 2: Use Environment Variables

Create `.env` file:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=employee_db
DATABASE_USER=db_user
DATABASE_PASSWORD=secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Install python-dotenv:
```bash
pip install python-dotenv
```

Update settings.py:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}
```

## Step 3: Install Production Dependencies

```bash
# PostgreSQL adapter
pip install psycopg2-binary

# MySQL adapter (alternative)
pip install mysqlclient

# Gunicorn (WSGI server)
pip install gunicorn

# Whitenoise (static files serving)
pip install whitenoise

# Environment variables
pip install python-dotenv
```

Update requirements.txt:
```
Django==5.2.15
sqlparse==0.5.5
asgiref==3.11.1
tzdata==2026.2
gunicorn==20.1.0
whitenoise==6.4.0
psycopg2-binary==2.9.6
python-dotenv==0.20.0
```

## Step 4: Configure Static Files

Add to settings.py:
```python
# Whitenoise middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

# Static files compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Collect static files:
```bash
python manage.py collectstatic --no-input
```

## Step 5: Set Up Gunicorn

Create `gunicorn_config.py`:
```python
import multiprocessing

bind = '127.0.0.1:8000'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2
```

Test Gunicorn:
```bash
gunicorn --config gunicorn_config.py employee_management.wsgi:application
```

## Step 6: Set Up Nginx (Reverse Proxy)

Create `/etc/nginx/sites-available/employee_management`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Nginx logging
    access_log /var/log/nginx/employee_management_access.log;
    error_log /var/log/nginx/employee_management_error.log;

    # Client upload limit
    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /var/www/employee_management/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/employee_management/media/;
        expires 7d;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/employee_management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 7: Set Up Systemd Service

Create `/etc/systemd/system/employee-management.service`:
```ini
[Unit]
Description=Employee Management System
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/employee_management
ExecStart=/var/www/employee_management/env/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    --config /var/www/employee_management/gunicorn_config.py \
    employee_management.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable employee-management.service
sudo systemctl start employee-management.service
sudo systemctl status employee-management.service
```

## Step 8: Set Up Database

For PostgreSQL:
```bash
# Create database
createdb employee_db

# Create user
createuser db_user
psql
ALTER USER db_user WITH PASSWORD 'secure_password';
ALTER ROLE db_user SET client_encoding TO 'utf8';
ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE employee_db TO db_user;
\q
```

Apply migrations:
```bash
python manage.py migrate
python manage.py createsuperuser
```

## Step 9: Set Up SSL Certificate

Using Let's Encrypt:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

Auto-renew certificates:
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Step 10: Run Security Checks

```bash
python manage.py check --deploy
```

Fix any security warnings reported.

## Step 11: Set Up Monitoring & Logging

Install Sentry (error tracking):
```bash
pip install sentry-sdk
```

Update settings.py:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False
)
```

## Step 12: Backup Strategy

Daily backup script (`/usr/local/bin/backup_employee_db.sh`):
```bash
#!/bin/bash

BACKUP_DIR="/var/backups/employee_management"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/employee_db_$DATE.sql"

mkdir -p $BACKUP_DIR

# PostgreSQL backup
pg_dump -U db_user -h localhost employee_db | gzip > "$BACKUP_FILE.gz"

# Keep only last 7 days
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

Add to crontab:
```bash
0 2 * * * /usr/local/bin/backup_employee_db.sh
```

## Step 13: Performance Optimization

### Caching
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Database Optimization
```python
# Add indexes to frequently queried fields
class Employee(models.Model):
    # ...
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['department']),
        ]
```

### Query Optimization
```python
# Use select_related() and prefetch_related()
employees = Employee.objects.select_related('department').all()
```

## Deployment Commands

```bash
# Pull latest code
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart employee-management.service

# Check status
sudo systemctl status employee-management.service
```

## Troubleshooting

### Check Systemd logs
```bash
sudo journalctl -u employee-management.service -f
```

### Check Nginx logs
```bash
sudo tail -f /var/log/nginx/employee_management_error.log
```

### Test Django settings
```bash
python manage.py check --deploy
```

### Restart all services
```bash
sudo systemctl restart nginx
sudo systemctl restart employee-management.service
```

## Monitoring Checklist

- [ ] Monitor disk space
- [ ] Monitor CPU usage
- [ ] Monitor memory usage
- [ ] Monitor database performance
- [ ] Monitor error logs
- [ ] Monitor uptime
- [ ] Check SSL certificate expiration
- [ ] Review user activity
- [ ] Backup verification

## Production Best Practices

1. **Security**
   - Use HTTPS everywhere
   - Keep Django updated
   - Use strong passwords
   - Enable 2FA
   - Regular security audits

2. **Performance**
   - Use CDN for static files
   - Enable caching
   - Optimize database queries
   - Use connection pooling
   - Monitor metrics

3. **Reliability**
   - Set up automated backups
   - Use load balancing
   - Configure monitoring/alerts
   - Implement error tracking
   - Regular testing

4. **Maintenance**
   - Keep dependencies updated
   - Regular code reviews
   - Document changes
   - Plan maintenance windows
   - Test deployments

---

**Last Updated:** 2024
**Version:** 1.0

For more help, consult Django deployment documentation:
https://docs.djangoproject.com/en/5.2/howto/deployment/
