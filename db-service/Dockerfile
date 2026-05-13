FROM postgres:16-alpine

LABEL maintainer="devops-practice"
LABEL service="db-service"

# Copy initialization scripts
COPY init/ /docker-entrypoint-initdb.d/

ENV POSTGRES_DB=votes
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

EXPOSE 5432

# Data directory for volume mounting
VOLUME ["/var/lib/postgresql/data"]

HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=5 \
  CMD pg_isready -U postgres -d votes || exit 1
