from fastapi import FastAPI, HTTPException, Request
from token_bucket import TokenBucket

class RateLimitFactory:
    @staticmethod
    def get_instance(algorithm:str = "TokenBucket"):
        if algorithm == "TokenBucket":
            return TokenBucket()
        else:
            raise HTTPException(status_code=404, detail="No algorithm specified")

    