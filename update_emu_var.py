import json
import os
import pickle
import requests
import pprint

from utils.credentials_loader import get_api_key
from utils.endpoints import RUNS_ENDPOINT
from utils.migration_utils import retrieve_target_runs
from utils.src_conversion_utils import format_run_for_post
from api.scoping import Scope

import id_data.game_ids as game_ids


def update_emu_runs(source_id, scope, key_path): 
    api_key = get_api_key(key_path)
    DISC_VAL_ID = "5q8jj76l"
    EMU_VAL_ID = "mlnpp6n1"
    FORMAT_VAR_ID = "jlzrre58"

    print("Getting runs from SRC...")
    
    run_data = None
    if os.path.exists("run_data"):
        # Load runs from disk
        print("Run data found on disk. Using this data.")
        with open('run_data', 'rb') as fp:
            run_data = pickle.load(fp)    
    else:
        # Retrieve run ids by network
        run_data = retrieve_target_runs(source_id, scope)
        with open('run_data', 'wb') as output_file:
            pickle.dump(run_data, output_file)

    print("Runs retrieved.")

    # Find runs that need to be tagged as Emu
    emu_run_data = []
    for run in run_data:
        is_emu_run = run["system"]["emulated"]
        if is_emu_run:
            variables = {
                FORMAT_VAR_ID: {
                    "type": "pre-defined",
                    "value": EMU_VAL_ID
                }
            }
            post_data = format_run_for_post(run, variables)
            


            # Append data for debugging
            emu_run_data.append((post_data, run["id"]))

    with open("emu_run_data.txt", "w+") as run_fp:
        pprint.pprint(emu_run_data, stream=run_fp)

    # Fill in auth headers
    headers = {
        "X-API-Key": api_key
    }
    test_data = emu_run_data[0]
    player_data = {
        "players": test_data[0]["run"].pop("players")
    }
    response = requests.post(url=RUNS_ENDPOINT, headers=headers, json=test_data[0])
    response.raise_for_status()
    run = json.loads(response.content.decode('utf-8'))
    
    run_id = run["data"]["id"]
    print(run_id)
    print(player_data)
    response = requests.put(url=f"{RUNS_ENDPOINT}/{run_id}", headers=headers, json=player_data)
    pprint.pprint(response.content)
    response.raise_for_status()

if __name__ == "__main__":
    update_emu_runs(game_ids.BFBB, Scope.GameScope, "api_key.json")