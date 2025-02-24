import os

import redis
import rq

redis_conn = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))
queue = rq.Queue("log_queue", connection=redis_conn)

if __name__ == "__main__":
    worker = rq.Worker([queue], connection=redis_conn)
    worker.work()
