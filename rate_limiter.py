from fastapi import FastAPI, HTTPException, Request
from sliding_window import SlidingWindow
from sliding_window_counter import SlidingWindowCounter
from token_bucket import TokenBucket
from fixed_counter_window import FixedCounterWindow

class RateLimitFactory:
    @staticmethod
    def get_instance(algorithm:str, ip):
        if algorithm == "TokenBucket":
            return TokenBucket()
        elif algorithm == "FixedCounterWindow":
            return FixedCounterWindow()
        elif algorithm == "SlidingWindow":
            return SlidingWindow()
        else:
            return SlidingWindowCounter(ip)

    