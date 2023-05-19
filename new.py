import redis
from apscheduler.schedulers.background import BackgroundScheduler


def job():
    # Your job code here
    pass


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', seconds=10)

redis_client = redis.Redis(host='redis', port=6379)

lock = redis_client.lock('my_lock', timeout=60)
if lock.acquire(blocking=False):
    scheduler.start()
    lock.release()
