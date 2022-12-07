# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, CloudBlue
# All rights reserved.
#
import pytest

from connect_ext.events import FulfillmentAutomationTestingEventsApplication


@pytest.mark.asyncio
async def test_handle_asset_purchase_request_processing(
    async_connect_client,
    async_client_mocker_factory,
    logger,
    mocker,
):
    request = {
        'id': 'PR-123',
        'template': {'id': 'TPL-123'},
        'asset': {
            'id': 'AS-123',
            'product': {'id': 'PRD-123'},
        },
        'status': 'pending',
    }
    client = async_client_mocker_factory()
    client.requests[request['id']]('approve').post(
        return_value={},
        match_body={'template_id': 'TPL-123'},
    )
    mocked_func = mocker.patch(
        'connect_ext.events.create_adjustment_request',
        mocker.AsyncMock(),
    )
    ext = FulfillmentAutomationTestingEventsApplication(async_connect_client, logger, {})
    result = await ext.handle_asset_purchase_request_processing(request)
    assert result.status == 'success'
    mocked_func.assert_awaited_with(ext.client, 'PRD-123', 'AS-123')


@pytest.mark.asyncio
async def test_handle_asset_purchase_request_validation(
    async_connect_client,
    logger,
):
    request = {'id': 'PR-123'}
    ext = FulfillmentAutomationTestingEventsApplication(async_connect_client, logger, {})
    result = await ext.handle_asset_purchase_request_validation(request)
    assert result.status == 'success'
    assert result.body == request


@pytest.mark.asyncio
async def test_handle_asset_suspend_request_processing(
    async_connect_client,
    logger,
    mocker,
):
    request = {'id': 'PR-123'}
    mocked_func = mocker.patch('connect_ext.events.purchase_request_approve', mocker.AsyncMock())
    ext = FulfillmentAutomationTestingEventsApplication(async_connect_client, logger, {})
    result = await ext.handle_asset_suspend_request_processing(request)
    assert result.status == 'success'
    mocked_func.assert_awaited_with(ext.client, request['id'])


@pytest.mark.asyncio
async def test_handle_asset_resume_request_processing(
    async_connect_client,
    logger,
    mocker,
):
    request = {'id': 'PR-123'}
    mocked_func = mocker.patch('connect_ext.events.purchase_request_approve', mocker.AsyncMock())
    ext = FulfillmentAutomationTestingEventsApplication(async_connect_client, logger, {})
    result = await ext.handle_asset_resume_request_processing(request)
    assert result.status == 'success'
    mocked_func.assert_awaited_with(ext.client, request['id'])


@pytest.mark.asyncio
async def test_handle_asset_cancel_request_processing(
    async_connect_client,
    logger,
    mocker,
):
    request = {'id': 'PR-123'}
    mocked_func = mocker.patch('connect_ext.events.purchase_request_approve', mocker.AsyncMock())
    ext = FulfillmentAutomationTestingEventsApplication(async_connect_client, logger, {})
    result = await ext.handle_asset_cancel_request_processing(request)
    assert result.status == 'success'
    mocked_func.assert_awaited_with(ext.client, request['id'])


@pytest.mark.asyncio
async def test_handle_asset_change_request_processing(
    async_connect_client,
    logger,
    mocker,
):
    request = {'id': 'PR-123'}
    mocked_func = mocker.patch('connect_ext.events.purchase_request_approve', mocker.AsyncMock())
    ext = FulfillmentAutomationTestingEventsApplication(async_connect_client, logger, {})
    result = await ext.handle_asset_change_request_processing(request)
    assert result.status == 'success'
    mocked_func.assert_awaited_with(ext.client, request['id'])


@pytest.mark.asyncio
async def test_handle_asset_adjustment_request_processing(
    async_connect_client,
    logger,
    mocker,
):
    request = {'id': 'PR-123'}
    mocked_func = mocker.patch('connect_ext.events.purchase_request_approve', mocker.AsyncMock())
    ext = FulfillmentAutomationTestingEventsApplication(async_connect_client, logger, {})
    result = await ext.handle_asset_adjustment_request_processing(request)
    assert result.status == 'success'
    mocked_func.assert_awaited_with(ext.client, request['id'])
