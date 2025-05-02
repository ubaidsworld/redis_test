import redis
import time
import logging
from datetime import datetime
import os
# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
REDIS_HOST = os.getenv("REDIS_HOST")  # e.g., "ec2-3-90-55-125.compute-1.amazonaws.com"
REDIS_PORT = 6379
REDIS_PASSWORD = None  # Set if you use AUTH
KEY_PREFIX = "test:heartbeat:"
TTL_SECONDS = 60  # Expire each key in 60 seconds
INTERVAL = 1  # Send data every 5 seconds

# Connect to Redis
try:
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        socket_connect_timeout=5,
        socket_timeout=5,
        decode_responses=True
    )
    r.ping()
    logging.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
except redis.RedisError as e:
    logging.error(f"Failed to connect to Redis: {e}")
    exit(1)

# Main loop
for i in range(60):
    try:
        timestamp = datetime.utcnow().isoformat()
        key = f"{KEY_PREFIX}{timestamp}"
        value = f"ping at {timestamp}"
        r.set(key, value, ex=TTL_SECONDS)
        logging.info(f"SET {key} → {value} (expires in {TTL_SECONDS}s)")
    except redis.RedisError as e:
        logging.error(f"Redis error: {e}")

    time.sleep(INTERVAL)
