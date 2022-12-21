# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, CloudBlue
# All rights reserved.
#
async def purchase_request_approve(client, request_id):
    request = await client.requests[request_id].get()
    template_id = request['template']['id']
    effective_date = request['created']
    body = {'template_id': template_id, 'effective_date': effective_date}
    response = await client.requests[request_id]('approve').post(payload=body)
    return response


async def create_adjustment_request(client, product_id, asset_id):
    params = [p async for p in client.products[product_id].parameters.all()]
    body = {
        'type': 'adjustment',
        'asset': {
            'id': asset_id,
            'params': params,
        },
    }
    response = await client.requests.create(payload=body)
    return response
