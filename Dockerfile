# Dockerfile
FROM python:3.12-alpine

WORKDIR /app

# Install OS packages
RUN apk add --no-cache \
    gcc musl-dev libpq-dev

# Copy essentials
COPY requirements.txt .
COPY manage.py .
COPY . /app
COPY entrypoint.py .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create directories for mounting (se vuoi montarli da host)
RUN mkdir -p /app/packages /app/fixtures /app/logs

CMD ["python", "entrypoint.py"]
