# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, CloudBlue
# All rights reserved.
#
from connect.eaas.core.decorators import (
    event,
)
from connect.eaas.core.extension import EventsApplicationBase
from connect.eaas.core.responses import (
    BackgroundResponse,
    InteractiveResponse,
)

from connect_ext.decorators import safe_client
from connect_ext.operations import (
    create_adjustment_request,
    purchase_request_approve,
)


class FulfillmentAutomationTestingEventsApplication(EventsApplicationBase):

    @safe_client()
    @event(
        'asset_purchase_request_processing',
        statuses=[
            'pending',
        ],
    )
    async def handle_asset_purchase_request_processing(self, request):
        self.logger.info(
            f"handle_asset_purchase_request_processing {request['id']} {request['status']}",
        )
        request_id = request['id']
        template_id = request['template']['id']
        payload = {'template_id': template_id}
        await self.client.requests[request_id]('approve').post(payload=payload)
        await create_adjustment_request(
            self.client,
            request['asset']['product']['id'],
            request['asset']['id'],
        )
        return BackgroundResponse.done()

    @event(
        'asset_purchase_request_validation',
        statuses=[
            'draft', 'inquiring',
        ],
    )
    async def handle_asset_purchase_request_validation(self, request):
        self.logger.info(f"handle_asset_purchase_request_validation {request['id']}")
        return InteractiveResponse.done(
            http_status=200,
            headers={'X-Custom-Header': 'value'},
            body=request,
        )

    @safe_client()
    @event(
        'asset_suspend_request_processing',
        statuses=[
            'pending',
        ],
    )
    async def handle_asset_suspend_request_processing(self, request):
        self.logger.info(f"handle_asset_suspend_request_processing {request['id']}")
        await purchase_request_approve(self.client, request['id'])
        return BackgroundResponse.done()

    @safe_client()
    @event(
        'asset_resume_request_processing',
        statuses=[
            'pending',
        ],
    )
    async def handle_asset_resume_request_processing(self, request):
        self.logger.info(f"handle_asset_resume_request_processing {request['id']}")
        await purchase_request_approve(self.client, request['id'])
        return BackgroundResponse.done()

    @safe_client()
    @event(
        'asset_cancel_request_processing',
        statuses=[
            'pending',
        ],
    )
    async def handle_asset_cancel_request_processing(self, request):
        self.logger.info(f"handle_asset_cancel_request_processing {request['id']}")
        await purchase_request_approve(self.client, request['id'])
        return BackgroundResponse.done()

    @safe_client()
    @event(
        'asset_change_request_processing',
        statuses=[
            'pending',
        ],
    )
    async def handle_asset_change_request_processing(self, request):
        self.logger.info(f"handle_asset_change_request_processing {request['id']}")
        await purchase_request_approve(self.client, request['id'])
        return BackgroundResponse.done()

    @safe_client()
    @event(
        'asset_adjustment_request_processing',
        statuses=[
            'pending',
        ],
    )
    async def handle_asset_adjustment_request_processing(self, request):
        self.logger.info(f"handle_asset_adjustment_request_processing {request['id']}")
        await purchase_request_approve(self.client, request['id'])
        return BackgroundResponse.done()
