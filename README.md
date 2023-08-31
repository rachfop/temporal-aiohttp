# README

This is an example of a REST API using [AIOHTTP](https://docs.aiohttp.org) and Python which implements a simplified form of one-click buying where a purchase is started and then, unless cancelled, will be performed in 10 seconds.

The bases of this repository are from the blog post announcement for the [Temporal Python SDK](https://temporal.io/blog/durable-distributed-asyncio-event-loop).

## Getting started

To get started, run the following commands:

```bash
# termianl 1
poetry run python run_worker.py
# terminal 2
poetry run python run_workflow.py
```

Then you can make requests to the API:

```bash
curl -X POST http://localhost:5001/purchase -H "Content-Type: application/json" -d '{"item_id": "item1", "user_id": "user1"}'
```
