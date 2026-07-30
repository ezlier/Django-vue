FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (mysqlclient build deps + curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 120

COPY . .

# Collect static files (need a dummy SECRET_KEY at build time)
RUN DJANGO_SECRET_KEY=build-time-only python manage.py collectstatic --noinput

# Create non-root user
RUN groupadd -r django && useradd -r -g django django && \
    chown -R django:django /app

USER django

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

CMD ["gunicorn", "djangoProject.wsgi:application", "--bind", "0.0.0.0:8000"]
