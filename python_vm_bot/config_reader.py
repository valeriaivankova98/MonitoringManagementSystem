import json

with open('config.json', 'r') as f:
    config = json.load(f)


def read_config_key(key):
    if key in config:
        return config[key]
    return None
