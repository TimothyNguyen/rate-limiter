from datetime import datetime, timedelta
import asyncio
from rate_limit_dto import RateLimit, RateLimitExceeded


class TokenBucket(RateLimit):
    def __init__(self, capacity: int = 10, refill_rate: float = 1):
        """
        Initialize the token bucket.

        Args:
            capacity (int): Maximum number of tokens the bucket can hold.
            refill_rate (float): Rate at which tokens are added (tokens per second).
        """
        super().__init__()
        self.token_capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.bucket_semaphore = asyncio.Semaphore(1)
        # Token bucket state
        self.last_refill = datetime.now()

    
    async def allow_request(self):
        """
        Consumes a token if available; otherwise raises an exception.

        Raises:
            HTTPException: If no tokens are available.
        """
        async with self.bucket_semaphore:
            current_time = datetime.now()
            elapsed_time = (current_time - self.last_refill).total_seconds()
            tokens_to_add = elapsed_time * self.refill_rate
            self.tokens = min(self.token_capacity, self.tokens + tokens_to_add)
            self.last_refill = current_time
        
        print(self.tokens)

        async with self.bucket_semaphore:
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            raise RateLimitExceeded()