#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import json

NUM_UNIQ_ENDPOINTS = 10000

CUSTOMIZATION = {}

# # response with 30s
# for endpoint in range(0, 2000):
#     CUSTOMIZATION[endpoint] = {
#         "lag": 30,
#     }

# # response with 45s
# for endpoint in range(2000, 3000):
#     CUSTOMIZATION[endpoint] = {
#         "lag": 45,
#     }

# # response 5xx/4xx error
# for endpoint in range(3000, 3100):
#     CUSTOMIZATION[endpoint] = {
#         "code": random.choice((401, 404, 500, 502, 503))
#     }

# response with const seq
for endpoint in range(3100, 3200):
    CUSTOMIZATION[endpoint] = {
        "apply_const_seq": True,
    }

# response with status->!status->status...
for endpoint in range(3200, NUM_UNIQ_ENDPOINTS):
    CUSTOMIZATION[endpoint] = {
        "apply_alternate_status": True,
    }


def default_endpoint_behaviour(cusotomization=None):
    if not cusotomization:
        cusotomization = {}
    behaviour = {
        "seq": 1,
        "code": 200,
        "status": random.choice((True, False)),
        "lag": random.randrange(0, 100) / 1000,
        "apply_alternate_status": False,
        "apply_const_seq": False,
    }
    behaviour.update(cusotomization)
    return behaviour


state = {}

for endpoint in range(NUM_UNIQ_ENDPOINTS):
    behaviour_customization = CUSTOMIZATION.get(endpoint)
    endpoint_behaviour = default_endpoint_behaviour(behaviour_customization)
    state.update({endpoint: endpoint_behaviour})

with open("server_behaviour.json", "w+") as state_f:
    json.dump(state, state_f, indent=2)