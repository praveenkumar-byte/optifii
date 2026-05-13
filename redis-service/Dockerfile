FROM redis:7.2-alpine

LABEL maintainer="devops-practice"
LABEL service="redis-service"

# Copy custom config
COPY redis.conf /usr/local/etc/redis/redis.conf

# Create data directory
RUN mkdir -p /data && chown redis:redis /data

EXPOSE 6379

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD redis-cli ping | grep -q PONG || exit 1

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
