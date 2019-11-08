import credentials_loader
from migration_utils import get_target_runs, post_runs
import game_ids

def move_runs(source_category_id, target_category_id, api_key_path):
    try:
        api_key = credentials_loader.get_api_key(api_key_path)

        # Get runs and copy them to be POSTed to new location
        existing_runs = get_target_runs(source_category_id)

        # Start posting them to a new board
        post_runs(existing_runs)
        
    except Exception as ex:
        print("Error migrating runs. The following exception occurred:")
        print(ex.with_traceback)

if __name__ == "__main__":
    runs = get_target_runs(game_ids.C_TSSM_CHEATPERCENT)
    print(runs[0])
