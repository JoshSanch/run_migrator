import credentials_loader
from migration_utils import get_target_runs, generate_run_request_data, dump_runs, post_formatted_runs, RUNS_ENDPOINT
import game_ids

def move_runs(source_category_id, target_category_id, api_key_path):
    try:
        api_key = credentials_loader.get_api_key(api_key_path)

        # Get runs and copy them to be POSTed to new location
        existing_runs = get_target_runs(source_category_id)
        primed_runs = generate_run_request_data(existing_runs, target_id)

        # Start posting them to a new board
        post_formatted_runs(primed_runs, RUNS_ENDPOINT, api_key)
        
    except Exception as ex:
        print("Error migrating runs. The following exception occurred:")
        print(ex)

if __name__ == "__main__":
    source_id = game_ids.C_TSSM_CHEATPERCENT
    target_id = game_ids.C_TSSMCE_CHEATPERCENT

    move_runs(source_id, target_id, "api_key.json")
    
