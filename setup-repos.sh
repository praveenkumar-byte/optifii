#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# setup-repos.sh — Initialize 5 separate Git repositories
# Usage: chmod +x setup-repos.sh && ./setup-repos.sh
# ─────────────────────────────────────────────────────────────────

set -e

SERVICES=(
  "vote-service"
  "result-service"
  "worker-service"
  "redis-service"
  "db-service"
)

echo "🚀 Initializing separate Git repositories for each microservice..."
echo ""

for svc in "${SERVICES[@]}"; do
  echo "──────────────────────────────────"
  echo "📦 Setting up: $svc"
  echo "──────────────────────────────────"

  cd "$svc"

  # Initialize Git repo
  git init
  git checkout -b main

  # Stage all files
  git add .

  # Initial commit
  git commit -m "feat: initial commit for $svc

  - Added Dockerfile with health checks and non-root user
  - Added application source code
  - Added README with DevOps practice checklist
  - Ready for CI/CD pipeline integration"

  echo "✅ $svc initialized with $(git rev-list --count HEAD) commit(s)"
  echo ""

  cd ..
done

echo "══════════════════════════════════════"
echo "✅ All 5 repositories initialized!"
echo ""
echo "Next steps:"
echo "  1. Create remote repos on GitHub:"
echo "     gh repo create vote-service-repo --public"
echo "     gh repo create result-service-repo --public"
echo "     gh repo create worker-service-repo --public"
echo "     gh repo create redis-service-repo --public"
echo "     gh repo create db-service-repo --public"
echo ""
echo "  2. Add remotes and push:"
echo "     cd vote-service && git remote add origin <url> && git push -u origin main"
echo ""
echo "  3. Run locally:"
echo "     cd .. && docker compose up --build"
echo "══════════════════════════════════════"
