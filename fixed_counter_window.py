from datetime import datetime, timedelta
import asyncio
from rate_limit_dto import RateLimit, RateLimitExceeded


class FixedCounterWindow(RateLimit):
    def __init__(self, limit_per_interval: int = 10, time_interval: int = 30):
        """
        Initialize the token bucket.

        Args:
            limit_per_interval (int): Maximum number of requests in an interval
            time_interval (int): Fixed time interval
        """
        super().__init__()
        self.counter = 0
        self.start_time = datetime.now()
        self.limit_per_interval = limit_per_interval
        self.time_interval = time_interval
        self.bucket_semaphore = asyncio.Semaphore(1)


    async def allow_request(self):
        """
        Allows request if number of requests in the window is less than the capacity; otherwise raises an exception.

        Raises:
            HTTPException: If no tokens are available.
        """
        async with self.bucket_semaphore:
            current_time = datetime.now()
            elapsed_time = (current_time - self.start_time).total_seconds()
            if elapsed_time >= self.time_interval:
                self.start_time = current_time
                self.counter = 0
            
            if self.counter >= self.limit_per_interval:
                raise RateLimitExceeded()
            
            self.counter += 1
            return True
            