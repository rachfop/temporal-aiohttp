import asyncio
from datetime import timedelta
from enum import IntEnum
from typing import Optional

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import Purchase, do_purchase


class PurchaseStatus(IntEnum):
    PENDING = 1
    CONFIRMED = 2
    CANCELLED = 3
    COMPLETED = 4


@workflow.defn
class OneClickBuyWorkflow:
    def __init__(self) -> None:
        self.status = PurchaseStatus.PENDING
        self.purchase: Optional[Purchase] = None

    @workflow.run
    async def run(self, purchase: Purchase) -> PurchaseStatus:
        self.purchase = self.purchase or purchase

        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            self.status = PurchaseStatus.CANCELLED
            return self.status

        self.status = PurchaseStatus.CONFIRMED
        await workflow.execute_activity(
            do_purchase,
            self.purchase,
            start_to_close_timeout=timedelta(minutes=1),
            cancellation_type=workflow.ActivityCancellationType.WAIT_CANCELLATION_COMPLETED,
        )
        self.status = PurchaseStatus.COMPLETED
        return self.status

    @workflow.signal
    def update_purchase(self, purchase: Purchase) -> None:
        self.purchase = purchase

    @workflow.query
    def current_status(self) -> PurchaseStatus:
        return self.status
