#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiohttp import web
import logging
import asyncio
from server_utils import get_initial_server_state

logging.basicConfig(level=logging.ERROR)

logger = logging.getLogger(__name__)

LISTEN_PORT = 8000

state = get_initial_server_state()

logger.info("Loaded endpoints: %i", len(state))

routes = web.RouteTableDef()


@routes.get("/{endpoint_id}")
async def health_check(request):
    try:
        endpoint_id = int(request.match_info["endpoint_id"])
    except ValueError:
        endpoint_id = None

    if endpoint_id not in state:
        return web.json_response({"error": True}, status=422)

    response_ctx = state[endpoint_id]

    response = web.json_response(
        {
            "seq": response_ctx["seq"],
            "status": response_ctx["status"],
        },
        status=response_ctx["code"],
    )
    if response_ctx["apply_alternate_status"]:
        state[endpoint_id]["status"] = not response_ctx["status"]

    if 200 <= response_ctx["code"] < 300 and not state[endpoint_id]["apply_const_seq"]:
        state[endpoint_id]["seq"] += 1

    await asyncio.sleep(response_ctx["lag"])

    return response


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=LISTEN_PORT)
