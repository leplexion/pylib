import asyncio
from typing import Coroutine

def asyncRunMany(*asyncList:Coroutine):
    async def run(*asyncList):
        taskList = [asyncio.create_task(item) for item in asyncList]
        await asyncio.gather(*taskList)
    asyncio.run(run(*asyncList))

def asleep(sec:float): return asyncio.sleep(sec)