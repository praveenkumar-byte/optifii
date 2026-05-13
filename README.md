# 🗳️ Voting App — Microservices for DevOps Practice

A production-grade microservice voting application designed for hands-on DevOps practice.
Cast votes → Redis queues them → Worker persists to Postgres → Result dashboard shows live totals.

## 🏗️ Architecture

```
                    ┌─────────────────────────────────────────┐
                    │              FRONTEND NETWORK            │
                    │                                         │
  [User: Vote]───►  │  vote-service:5000  (Python/Flask)      │
                    │         │                               │
  [User: Results]─► │  result-service:4000 (Node.js/Socket.IO)│
                    └──────────┬───────────────┬─────────────┘
                               │               │
                    ┌──────────▼───────────────▼─────────────┐
                    │              BACKEND NETWORK            │
                    │                                         │
                    │  redis-service:6379  (Redis 7.2)        │
                    │         │                               │
                    │  worker-service      (Python)           │
                    │         │                               │
                    │  db-service:5432     (PostgreSQL 16)    │
                    └─────────────────────────────────────────┘
```

## 📁 Repository Structure

| Repository            | Language    | Port  | Role                          |
|-----------------------|-------------|-------|-------------------------------|
| `vote-service-repo`   | Python/Flask| 5000  | Accepts user votes             |
| `result-service-repo` | Node.js     | 4000  | Displays live results          |
| `worker-service-repo` | Python      | —     | Moves votes Redis → PostgreSQL |
| `redis-service-repo`  | Redis       | 6379  | Message queue                  |
| `db-service-repo`     | PostgreSQL  | 5432  | Persistent vote storage        |

## 🚀 Quick Start (Docker Compose)

```bash
# Clone this root repo
git clone <this-repo>
cd microservices

# Build and start all services
docker compose up --build

# Visit:
# Vote:    http://localhost:5000
# Results: http://localhost:4000
```

## ☸️ Kubernetes Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/voting-app.yaml

# Check status
kubectl get all -n voting-app

# Access (minikube example)
minikube service vote -n voting-app
minikube service result -n voting-app
```

## 🎯 DevOps Practice Roadmap

### Level 1 — Containers
- [ ] Build all 5 images locally
- [ ] Run with docker compose
- [ ] Understand network segmentation (frontend/backend)
- [ ] Explore health checks and restart policies

### Level 2 — CI/CD
- [ ] Push all images to DockerHub or GHCR
- [ ] Set up GitHub Actions pipeline for each service
- [ ] Add automated tests
- [ ] Implement semantic versioning + image tagging

### Level 3 — Kubernetes
- [ ] Deploy to a local cluster (minikube / kind)
- [ ] Use ConfigMaps and Secrets
- [ ] Add Ingress + TLS (cert-manager)
- [ ] Practice rolling updates: `kubectl set image ...`
- [ ] Practice rollback: `kubectl rollout undo`

### Level 4 — Observability
- [ ] Add Prometheus + Grafana
- [ ] Ship logs to ELK or Loki
- [ ] Trace requests with Jaeger or Tempo
- [ ] Set up alerting rules

### Level 5 — Production Hardening
- [ ] Horizontal Pod Autoscaling (HPA)
- [ ] PodDisruptionBudgets
- [ ] Network Policies
- [ ] PostgreSQL read replica
- [ ] Redis Sentinel / Cluster
- [ ] Secret management with Vault or Sealed Secrets

## 🔁 Data Flow (step by step)

1. User opens `http://localhost:5000` and clicks **Cats** or **Dogs**
2. `vote-service` pushes `{"voter_id": "abc123", "vote": "a"}` to Redis list `votes`
3. `worker-service` `BLPOP`s the message, upserts it into PostgreSQL `votes` table
4. `result-service` polls PostgreSQL every 1s, emits results over WebSocket
5. User's browser on `http://localhost:4000` sees the bar chart update live

## 🛠️ Environment Variables Reference

See each service's README for detailed env var documentation.
All defaults work out-of-the-box with docker compose.
