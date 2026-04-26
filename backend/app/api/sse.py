import asyncio
import json
from typing import AsyncGenerator

class SSEQueue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def put_progress(self, stage_idx: int, total: int, status: str, message: str, elapsed: float):
        data = {
            "stage_idx": stage_idx,
            "total": total,
            "status": status,
            "message": message,
            "elapsed": elapsed
        }
        await self.queue.put(("progress", data))

    async def put_result(self, state_dict: dict):
        await self.queue.put(("result", state_dict))

    async def put_error(self, error_msg: str):
        await self.queue.put(("error", {"message": error_msg}))

    async def generator(self) -> AsyncGenerator[str, None]:
        while True:
            event_type, data = await self.queue.get()
            yield f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
            if event_type in ("result", "error"):
                break
