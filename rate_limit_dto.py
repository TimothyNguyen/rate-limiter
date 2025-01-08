from datetime import datetime, timedelta
import threading
from fastapi import HTTPException

class RateLimit:
    def __init__(self):
        self.interval = 30
        self.limit_per_interval = 30

class RateLimitExceeded(HTTPException):
    def __init__(self):
        super().__init__(status_code=429, detail="Rate limit exceeded")