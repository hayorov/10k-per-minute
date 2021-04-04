#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

NUM_ENDPOINTS = 10000

endpoint_pool = random.choices(
    list(range(0, NUM_ENDPOINTS)), weights=None, cum_weights=None, k=NUM_ENDPOINTS
)

with open("endpoints.txt", "w+") as cnt:
    cnt.write("\n".join([f"/{item}" for item in endpoint_pool]))