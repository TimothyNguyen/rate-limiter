from datetime import datetime, timedelta
import asyncio
from rate_limit_dto import RateLimit, RateLimitExceeded


class SlidingWindow(RateLimit):
    def __init__(self, limit_per_interval: int = 60, time_interval: int = 60):
        """
        Initialize the token bucket.

        Args:
            limit_per_interval (int): Maximum number of requests in an interval
            time_interval (int): Fixed time interval
        """
        super().__init__()
        self.window_logs = []
        self.limit_per_interval = limit_per_interval
        self.time_interval = time_interval
        self.bucket_semaphore = asyncio.Semaphore(1)


    async def allow_request(self):
        """
        Allows request if number of requests in the window is less than the capacity; otherwise raises an exception.

        Raises:
            HTTPException: If no tokens are available.
        """
        while await self.bucket_semaphore:
            current_time = datetime.now()
            while len(self.window_logs) > 0 and (current_time - self.window_logs[0]).total_seconds() >= self.time_interval: 
                self.window_logs.pop(0)
            
            if len(self.window_logs) >= self.limit_per_interval:
                raise RateLimitExceeded()
            
            self.window_logs.append(current_time)
            return True
            