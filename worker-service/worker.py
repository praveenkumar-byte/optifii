import redis
import psycopg2
import os
import json
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# ─── Config ──────────────────────────────────────────────────────────────────
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME", "votes")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

POLL_INTERVAL = float(os.environ.get("POLL_INTERVAL", 0.1))


def connect_redis():
    while True:
        try:
            r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
            r.ping()
            log.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
            return r
        except redis.ConnectionError as e:
            log.warning(f"Redis not ready: {e}. Retrying in 2s...")
            time.sleep(2)


def connect_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            conn.autocommit = False
            log.info(f"Connected to PostgreSQL at {DB_HOST}:{DB_PORT}")
            return conn
        except psycopg2.OperationalError as e:
            log.warning(f"DB not ready: {e}. Retrying in 2s...")
            time.sleep(2)


def ensure_schema(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id    VARCHAR(255) NOT NULL UNIQUE,
                vote  VARCHAR(255) NOT NULL
            );
        """)
        conn.commit()
    log.info("Database schema ensured.")


def process_vote(conn, voter_id: str, vote: str):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO votes (id, vote) VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE SET vote = EXCLUDED.vote;
        """, (voter_id, vote))
    conn.commit()
    log.info(f"Processed vote: voter={voter_id}, choice={vote}")


def main():
    log.info("Worker service starting...")
    r = connect_redis()
    conn = connect_db()
    ensure_schema(conn)

    log.info("Polling Redis queue 'votes'...")
    while True:
        try:
            # BLPOP blocks until a message arrives (timeout=0 = forever)
            result = r.blpop("votes", timeout=5)
            if result:
                _, raw = result
                data = json.loads(raw)
                voter_id = data["voter_id"]
                vote = data["vote"]
                process_vote(conn, voter_id, vote)
        except (redis.ConnectionError, redis.TimeoutError) as e:
            log.error(f"Redis connection lost: {e}. Reconnecting...")
            r = connect_redis()
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            log.error(f"DB connection lost: {e}. Reconnecting...")
            conn = connect_db()
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
