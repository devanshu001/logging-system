import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
import rq

engine = create_engine(os.getenv('DATABASE_URL'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Initialize Redis queue
redis_conn = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))
queue = rq.Queue("log_queue", connection=redis_conn)
