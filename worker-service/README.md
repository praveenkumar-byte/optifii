# worker-service

A Python background worker that continuously reads vote messages from Redis and persists them to PostgreSQL.

## 🏗️ Architecture Role
```
[redis-service:6379] → [worker-service] → [db-service:5432]
```

## ⚙️ Environment Variables

| Variable     | Default   | Description                |
|-------------|-----------|----------------------------|
| REDIS_HOST  | redis     | Redis hostname              |
| REDIS_PORT  | 6379      | Redis port                  |
| DB_HOST     | db        | PostgreSQL hostname          |
| DB_PORT     | 5432      | PostgreSQL port              |
| DB_NAME     | votes     | Database name               |
| DB_USER     | postgres  | DB username                 |
| DB_PASSWORD | postgres  | DB password                 |

## 🐳 DevOps Practice Tasks
- [ ] Add structured JSON logging for log aggregation (ELK / Loki)
- [ ] Create Kubernetes Deployment manifest (no Service needed)
- [ ] Set restart policy to `Always`
- [ ] Mount DB password from a Kubernetes Secret
- [ ] Add dead-letter queue for failed messages
- [ ] Set up alerting when queue depth spikes
- [ ] Benchmark throughput (votes/sec)
