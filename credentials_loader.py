import json

def get_api_key(api_key_file):
    with open(api_key_file) as key_data:
        return key_data["key"]