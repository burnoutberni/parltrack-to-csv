#!/usr/bin/env bash
curl "https://parltrack.org/dumps/ep_meps.json.lz" | lzip -d -o ep_meps.json
