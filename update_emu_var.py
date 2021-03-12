import json
import os
import pickle
import requests

from utils.credentials_loader import get_api_key
from utils.migration_utils import RUNS_ENDPOINT, CATEGORIES_ENDPOINT, retrieve_target_runs
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
    emulated_run_ids = []
    for run in run_data:
        is_emu_run = run["system"]["emulated"]
        if is_emu_run:
            emulated_run_ids.append(run["id"])

    # 


if __name__ == "__main__":
    update_emu_runs(game_ids.BFBB, Scope.GameScope, "api_key.json")

    test_run_id = "zx6xnjgz"
    endpoint_url = f"https://www.speedrun.com/api/v1/runs/{test_run_id}/status"
    response = requests.put(url=endpoint_url)
    response.raise_for_status()

    print(response)