# result-service

A Node.js + Express app that displays real-time vote counts using WebSockets (Socket.IO), polling PostgreSQL every second.

## 🏗️ Architecture Role
```
[db-service:5432] ← polls every 1s ← [result-service:4000] → WebSocket → [User Browser]
```

## ⚙️ Environment Variables

| Variable      | Default   | Description               |
|--------------|-----------|---------------------------|
| DB_HOST      | db        | PostgreSQL hostname         |
| DB_PORT      | 5432      | PostgreSQL port             |
| DB_NAME      | votes     | Database name              |
| DB_USER      | postgres  | DB username                |
| DB_PASSWORD  | postgres  | DB password                |
| PORT         | 4000      | HTTP port                  |
| POLL_INTERVAL| 1000      | DB poll interval (ms)      |

## 🐳 DevOps Practice Tasks
- [ ] Push to container registry
- [ ] Write Kubernetes Deployment + Service (NodePort/LoadBalancer)
- [ ] Configure ingress for external access
- [ ] Add Nginx reverse proxy in front
- [ ] Implement rate limiting
- [ ] Set up TLS with cert-manager
- [ ] Add WebSocket sticky sessions for k8s
