# 📊 Log Monitor - Quick Start

Django Log Monitoring & Anomaly Detection System.

---

## 🚀 Run Project

### Docker (Recommended)
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
# Access: http://localhost:8000/api/
```

### Local
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 📍 Main URLs

| URL | Purpose |
|-----|---------|
| `/api/` | Dashboard |
| `/api/send/` | Submit logs |
| `/api/logs/list/` | View logs |
| `/api/anomalies/` | View anomalies |
| `/admin/` | Admin panel |

---

## 📝 Submit Logs

**Web Form**: http://localhost:8000/api/send/

**REST API**:
```bash
curl -X POST http://localhost:8000/api/logs/ \
  -H "Content-Type: application/json" \
  -d '{"service":"auth-service","log_level":"ERROR","message":"Failed"}'
```

**Python**:
```python
import requests
requests.post("http://localhost:8000/api/logs/", json={
    "service": "auth-service",
    "log_level": "ERROR",
    "message": "Failed"
})
```

---

## ⚙️ Email Setup

1. Enable 2FA on Gmail
2. Get App Password: https://myaccount.google.com/apppasswords
3. Update `.env`:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ALERT_RECEIVER_EMAIL=alert@example.com
```
4. Restart: `docker-compose restart web`

Test: http://localhost:8000/api/test-email/

---

## 🔍 How It Works

- **Logs** → Submitted via form/API → Stored in database
- **Detector** → Runs every 5 min → Counts errors
- **Anomaly** → If errors ≥ 5 → Triggers alert
- **Email** → Sent via Gmail SMTP
- **Dashboard** → Shows all logs & alerts

---

## 🛠️ Commands

```bash
# Logs
docker-compose logs -f web

# Django shell
docker-compose exec web python manage.py shell

# Migrations
docker-compose exec web python manage.py makemigrations

# Reset DB (dev)
docker-compose exec web python manage.py migrate logs zero
docker-compose exec web python manage.py migrate

# Tests
docker-compose exec web pytest

# Stop
docker-compose down
```

---

## 📊 Database Tables

| Table | Fields |
|-------|--------|
| **LogEntry** | service, log_level, message, timestamp |
| **Anomaly** | anomaly_type, severity, timestamp |
| **Alert** | anomaly, status, sent_at |

---

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| DB connection error | `docker-compose restart db` |
| Emails not sending | Check `.env` file & logs |
| Container won't start | `docker-compose build --no-cache && docker-compose up -d` |

---

**Error Threshold**: 5 | **Check Interval**: 5 min | **Email**: Gmail SMTP
