import asyncio

from aiohttp import web
from temporalio.client import Client

from activities import Purchase
from workflows import OneClickBuyWorkflow, PurchaseStatus


async def init_app():
    app = web.Application()
    app.client = await Client.connect("localhost:7233")
    app.router.add_post("/purchase", handle_purchase)
    return app


async def handle_purchase(request) -> web.Response:
    data = await request.json()
    print(f"Received purchase request: {data}")

    client = request.app.client
    handle = await client.start_workflow(
        OneClickBuyWorkflow.run,
        Purchase(
            item_id=data.get("item_id", "unknown"),
            user_id=data.get("user_id", "unknown"),
        ),
        id=f"{data.get('user_id', 'unknown')}-purchase1",
        task_queue="my-task-queue",
    )

    await handle.cancel()

    status = await handle.query(OneClickBuyWorkflow.current_status)
    assert status == PurchaseStatus.CANCELLED

    return web.json_response(
        {"status": "success", "workflow_status": status.name}, status=200
    )


if __name__ == "__main__":
    app = asyncio.run(init_app())
    web.run_app(app, port=5001)
