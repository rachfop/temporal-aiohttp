import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import do_purchase
from workflows import OneClickBuyWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[OneClickBuyWorkflow],
        activities=[do_purchase],
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
