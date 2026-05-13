FROM python:3.11-slim

LABEL maintainer="devops-practice"
LABEL service="worker-service"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Worker has no exposed port — it's a background processor
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD pgrep -f worker.py || exit 1

CMD ["python", "-u", "worker.py"]
