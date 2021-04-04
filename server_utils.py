# -*- coding: utf-8 -*-

import json


def get_initial_server_state():
    with open("server_behaviour.json") as state_f:
        return json.load(
            state_f,
            object_hook=lambda d: {
                int(k) if k.lstrip("-").isdigit() else k: v for k, v in d.items()
            },
        )
