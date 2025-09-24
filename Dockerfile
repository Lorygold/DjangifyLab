# Dockerfile
FROM python:3.12-slim-trixie

WORKDIR /app

# Install OS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libc6-dev \
    libpcre2-dev \
    libssl-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy essentials
COPY requirements.txt .
COPY manage.py .
COPY . /app
COPY entrypoint.py .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create directories for mounting (se vuoi montarli da host)
RUN mkdir -p /app/packages /app/fixtures /app/logs
