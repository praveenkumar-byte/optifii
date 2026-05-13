# redis-service

A pre-configured Redis 7.2 instance used as the message queue between vote-service and worker-service.

## 🏗️ Architecture Role
```
[vote-service] → RPUSH votes → [redis-service:6379] → BLPOP → [worker-service]
```

## Queue Structure
- **Key**: `votes` (List type)
- **Format**: JSON — `{"voter_id": "<hex>", "vote": "a"|"b"}`
- **Pattern**: RPUSH (producer) + BLPOP (consumer)

## 🐳 DevOps Practice Tasks
- [ ] Mount persistent volume for /data
- [ ] Use Kubernetes StatefulSet instead of Deployment
- [ ] Set up Redis Sentinel for HA
- [ ] Add Redis Exporter for Prometheus metrics
- [ ] Configure password auth (requirepass)
- [ ] Set up backup CronJob to S3
- [ ] Practice Redis cluster mode (3 masters + 3 replicas)

## 🔧 Useful Commands
```bash
# Monitor the queue in real time
redis-cli MONITOR

# Check queue depth
redis-cli LLEN votes

# Inspect messages
redis-cli LRANGE votes 0 -1

# Flush all (reset)
redis-cli FLUSHALL
```
