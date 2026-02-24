FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git docker.io \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir \
  celery==5.4.0 redis==5.0.8 sqlalchemy==2.0.34 psycopg[binary]==3.2.2

WORKDIR /app
COPY app ./app

CMD ["celery", "-A", "app.worker:celery_app", "worker", "--loglevel=INFO"]