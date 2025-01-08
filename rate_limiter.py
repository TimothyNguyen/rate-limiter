from fastapi import FastAPI, HTTPException, Request
from sliding_counter import SlidingWindow
from token_bucket import TokenBucket
from fixed_counter_window import FixedCounterWindow

class RateLimitFactory:
    @staticmethod
    def get_instance(algorithm:str = "TokenBucket"):
        if algorithm == "TokenBucket":
            return TokenBucket()
        elif algorithm == "FixedCounterWindow":
            return FixedCounterWindow()
        elif algorithm == "SlidingWindow":
            return SlidingWindow()
        else:
            raise HTTPException(status_code=404, detail="No algorithm specified")

    