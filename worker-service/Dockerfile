FROM python:3.11-slim AS builder

LABEL maintainer="devops-practice"
LABEL service="worker-service"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed Python packages and app code from builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

# RUN adduser --disabled-password --gecos '' appuser
# USER appuser

# Worker has no exposed port — it's a background processor

# Health check to ensure the worker process is running.
# --timeout=5s: Allow up to 5 seconds for the check to complete.
# --start-period=15s: Wait 15 seconds after the container starts before beginning health checks.
# --retries=3: Mark the container as unhealthy after 3 consecutive failed checks.
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD pgrep -f worker.py || exit 1

CMD ["python", "-u", "worker.py"]
