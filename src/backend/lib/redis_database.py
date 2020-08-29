import redis
import pickle

class RedisDatabase():
    def __init__(self, host, port, db):
        self._redis = redis.Redis(host, port, db)
    def get_data_manager(self):
        return pickle.load(self._redis.get("data_manager"))
    def get_crawl_queue(self):
        return pickle.load(self._redis.get("crawl_queue"))
    def set_data_manager(self, data_manager):
        self._redis.set("data_manager", pickle.dumps(data_manager))
    def set_crawl_queue(self, crawl_queue):
        self._redis.set("crawl_queue", pickle.dumps(crawl_queue))

