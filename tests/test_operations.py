# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, CloudBlue
# All rights reserved.
#
import pytest

from connect_ext.operations import create_adjustment_request, purchase_request_approve


@pytest.mark.asyncio
async def test_purchase_request_approve(
    async_connect_client,
    async_client_mocker_factory,
):
    request = {
        'id': 'PR-123',
        'template': {'id': 'TPL-123'},
        'asset': {
            'id': 'AS-123',
            'product': {'id': 'PRD-123'},
        },
        'status': 'pending',
        'created': '2022-01-01 10:10:10',
    }
    client = async_client_mocker_factory()
    client.requests[request['id']].get(return_value=request)
    client.products[request['asset']['product']['id']].parameters.filter(
        'required=true',
    ).mock(
        return_value=[{'name': 'param_a'}],
    )
    client.requests[request['id']].update(return_value={})
    client.requests[request['id']]('approve').post(
        return_value={'response': 'okay'},
        match_body={'template_id': 'TPL-123', 'effective_date': request['created']},
    )
    response = await purchase_request_approve(async_connect_client, request['id'])
    assert response == {'response': 'okay'}


@pytest.mark.asyncio
async def test_create_adjustment_request(
    async_connect_client,
    async_client_mocker_factory,
):
    product_id = 'PRD-123'
    asset_id = 'AS-123'
    client = async_client_mocker_factory()
    client.products[product_id].parameters.all().mock(
        return_value=[{'name': 'param_a'}],
    )
    expected_body = {
        'type': 'adjustment',
        'asset': {
            'id': asset_id,
            'params': [{'name': 'param_a'}],
        },
    }
    client.requests.create(return_value={'some': 'response'}, match_body=expected_body)
    response = await create_adjustment_request(async_connect_client, product_id, asset_id)
    assert response == {'some': 'response'}
