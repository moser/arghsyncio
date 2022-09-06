import time
import asyncio


async def wait(n):
    # good, async "IO"
    # await asyncio.sleep(2)
    # bad, sync "IO"
    time.sleep(2)
    print(n)


async def main():
    tasks = []
    for n in range(20):
        tasks.append(asyncio.create_task(wait(n)))
    await asyncio.gather(*tasks)


asyncio.run(main())
