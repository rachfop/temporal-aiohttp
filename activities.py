from dataclasses import asdict, dataclass

import aiohttp
from temporalio import activity
from temporalio.exceptions import ApplicationError


@dataclass
class Purchase:
    item_id: str
    user_id: str


@activity.defn
async def do_purchase(purchase: Purchase) -> None:
    async with aiohttp.ClientSession() as sess:
        async with sess.post(
            "http://localhost:5001/purchase", json=asdict(purchase)
        ) as resp:
            if resp.status >= 400 and resp.status < 500:
                raise ApplicationError(
                    f"Status: {resp.status}", resp.json(), non_retryable=True
                )
            resp.raise_for_status()
