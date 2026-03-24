FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 optifii

# Copy dependencies from builder
COPY --from=builder --chown=optifii:optifii /root/.local /home/optifii/.local

# Set PATH to include user's local bin
ENV PATH=/home/optifii/.local/bin:$PATH

# Copy application files
COPY --chown=optifii:optifii . .

# Switch to non-root user
USER optifii

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["python", "app.py"]