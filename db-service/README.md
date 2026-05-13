# db-service

PostgreSQL 16 database that persistently stores all votes. Schema is auto-initialized on first run.

## 🏗️ Architecture Role
```
[worker-service] → INSERT/UPSERT → [db-service:5432] ← SELECT → [result-service]
```

## Schema
```sql
CREATE TABLE votes (
    id   VARCHAR(255) NOT NULL UNIQUE,   -- voter_id (cookie)
    vote VARCHAR(255) NOT NULL           -- 'a' or 'b'
);
```
Each voter can only vote once — duplicate `id` values are upserted (UPDATE).

## ⚙️ Environment Variables (set at runtime)

| Variable            | Default   | Description        |
|--------------------|-----------|--------------------|
| POSTGRES_DB        | votes     | Database name       |
| POSTGRES_USER      | postgres  | Superuser name      |
| POSTGRES_PASSWORD  | postgres  | Superuser password  |

## 🐳 DevOps Practice Tasks
- [ ] Mount `/var/lib/postgresql/data` to a persistent volume
- [ ] Use Kubernetes StatefulSet + PersistentVolumeClaim
- [ ] Store POSTGRES_PASSWORD in a Kubernetes Secret
- [ ] Set up pg_dump CronJob for backups to S3/GCS
- [ ] Deploy read replica for result-service queries
- [ ] Add postgres-exporter for Prometheus metrics
- [ ] Practice point-in-time recovery (PITR) with WAL

## 🔧 Useful Commands
```bash
# Connect to the database
psql -U postgres -d votes

# Check vote counts
SELECT vote, COUNT(*) FROM votes GROUP BY vote;

# Total votes
SELECT COUNT(*) FROM votes;

# Reset all votes
DELETE FROM votes;
```
