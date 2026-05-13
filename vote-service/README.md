# vote-service

A Python/Flask web application that accepts votes from users and pushes them to a Redis queue.

## 🏗️ Architecture Role
```
[User Browser] → [vote-service:5000] → [redis-service:6379]
```

## 🚀 Quick Start

### Local Development
```bash
pip install -r requirements.txt
export REDIS_HOST=localhost
export REDIS_PORT=6379
export OPTION_A=Cats
export OPTION_B=Dogs
python app.py
```

### Docker
```bash
docker build -t vote-service:latest .
docker run -p 5000:5000 \
  -e REDIS_HOST=redis \
  -e OPTION_A=Cats \
  -e OPTION_B=Dogs \
  vote-service:latest
```

## ⚙️ Environment Variables

| Variable     | Default   | Description              |
|-------------|-----------|--------------------------|
| REDIS_HOST  | redis     | Redis service hostname   |
| REDIS_PORT  | 6379      | Redis service port       |
| OPTION_A    | Cats      | First voting option      |
| OPTION_B    | Dogs      | Second voting option     |

## 🏥 Health Check
```
GET /health → {"status": "healthy", "service": "vote"}
```

## 🐳 DevOps Practice Tasks
- [ ] Push image to DockerHub / ECR / GCR
- [ ] Write a Kubernetes Deployment + Service manifest
- [ ] Set up a CI pipeline (GitHub Actions / Jenkins)
- [ ] Add resource limits (cpu/memory)
- [ ] Configure horizontal pod autoscaling
- [ ] Add Prometheus metrics endpoint
- [ ] Set up liveness + readiness probes
