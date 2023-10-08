from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

import redis

import os


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


redis_password = os.getenv("REDIS_PASSWORD")

# Connect to Redis
r = redis.Redis(
    host='redis-18302.c293.eu-central-1-1.ec2.cloud.redislabs.com',
    port=18302,
    password=redis_password,
    decode_responses=True  # Decodes the bytes type to str
)


# Get Redis password from environment variables


@app.get("/set/{my_id}")
async def set_id(my_id: str):
    # Set value in Redis with expiration of 3600 seconds (1 hour)
    r.setex(my_id, 3600, "This is an example value")
    return {"status": "success", "message": "Value set successfully"}


@app.get("/get/{my_id}")
async def get_id(my_id: str):
    # Retrieve value from Redis
    value = r.get(my_id)

    # Check if value exists
    if value is None:
        raise HTTPException(status_code=404, detail="ID not found")

    return {"id": my_id, "value": value}

