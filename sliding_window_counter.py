from datetime import datetime
from cache import Cache
from rate_limit_dto import RateLimit, RateLimitExceeded

distributed_cache = Cache()

class SlidingWindowCounter(RateLimit):
    def __init__(self, ip):
        super().__init__()
        self.current_window_counter = 0
        self.prev_window_counter = 0
        self.curr_window = datetime.now()
        self.ip = ip
    
    def _rotate_counter(self):
        curr_time = datetime.now()
        self.prev_window_counter = self.current_window_counter if ((curr_time-self.curr_window).total_seconds()//60)==1 else 0
        self.current_window_counter = 0
        self.curr_window = curr_time
    
    async def allow_request(self):
        lock_acquired, lock_key = distributed_cache.acquire_lock(self.ip)
        if lock_acquired:
            self.current_window_counter,self.prev_window_counter,self.curr_window = distributed_cache.get_data(self.ip)
            seconds = datetime.now().second
            prev_window_reminder = self.limit_per_interval - seconds
            self._rotate_counter()
            limit = self.current_window_counter + int(self.prev_window_counter*(prev_window_reminder/60))
            
            print(limit)
            
            if limit >= self.limit_per_interval:
                distributed_cache.release_lock(lock_key)
                raise RateLimitExceeded()
            self.current_window_counter+=1
            distributed_cache.set_data(self.ip,self.current_window_counter,self.prev_window_counter,self.curr_window)
            distributed_cache.release_lock(lock_key)
            return True