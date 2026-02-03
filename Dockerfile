FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system certificates and tools
RUN apt-get update && apt-get install -y \
    ca-certificates \
    openssl \
    curl \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*


# Force Python & OpenSSL to use system certs
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_DIR=/etc/ssl/certs
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt


# Rebuild OpenSSL cert links (IMPORTANT FIX)
RUN c_rehash /etc/ssl/certs


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "log_monitor.wsgi:application", "--bind", "0.0.0.0:8000"]
