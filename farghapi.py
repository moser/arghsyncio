"""
Run with

    uvicorn farghapi:app --port 9999 --reload


$ ab -c 5 -n 10 http://localhost:9999/async_calls_sync | grep "Time taken"
Time taken for tests:   20.036 seconds

$ ab -c 5 -n 10 http://localhost:9999/async_calls_async | grep "Time taken"
Time taken for tests:   6.014 seconds

$ ab -c 5 -n 10 http://localhost:9999/sync_calls_sync | grep "Time taken"
Time taken for tests:   6.020 seconds

$ ab -c 5 -n 10 http://localhost:9999/async_calls_sync_correctly | grep "Time taken"
Time taken for tests:   6.019 seconds
"""

import time
import asyncio
from fastapi import FastAPI

app = FastAPI()


async def async_long_running_task():
    await asyncio.sleep(2)


def sync_long_running_task():
    time.sleep(2)


@app.get("/async_calls_sync")
async def a():
    print(">async_calls_sync")
    sync_long_running_task()
    print("<async_calls_sync")
    return {"Hello": "World"}


@app.get("/async_calls_async")
async def b():
    print(">async_calls_async")
    await async_long_running_task()
    print("<async_calls_async")
    return {"Hello": "World"}


@app.get("/sync_calls_sync")
def c():
    print(">sync_calls_sync")
    sync_long_running_task()
    print("<sync_calls_sync")
    return {"Hello": "World"}


@app.get("/async_calls_sync_correctly")
async def d():
    print(">async_calls_sync_correctly")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, sync_long_running_task)
    print("<async_calls_sync_correctly")
    return {"Hello": "World"}
