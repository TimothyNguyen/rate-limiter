from fastapi import FastAPI, Request
from rate_limiter import RateLimitFactory
from rate_limit_dto import RateLimitExceeded

app = FastAPI()
ip_addresses = {}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/limited")
async def limited(request: Request):
    client = request.client.host
    try:
        if client not in ip_addresses:
            ip_addresses[client] = RateLimitFactory.get_instance("TokenBucket")
            #ip_addresses[client] = RateLimitFactory.get_instance("FixedCounterWindow")
        if await ip_addresses[client].allow_request():
            return "This is a limited use API"
    except RateLimitExceeded as e:
        raise e