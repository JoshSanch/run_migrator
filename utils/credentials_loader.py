import json


def get_api_key(api_key_file):
    with open(api_key_file) as key_data:
        return json.load(key_data)["key"]
