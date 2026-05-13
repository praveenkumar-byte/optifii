FROM python:3.11-slim AS builder

LABEL maintainer="devops-practice"
LABEL service="vote-service"

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code into the builder image
COPY . .


FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed dependencies and application code from the builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Non-root user for security
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:app"]
