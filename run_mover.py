from utils.credentials_loader import get_api_key
from utils.migration_utils import retrieve_target_runs, generate_run_request_data, dump_runs, post_formatted_runs, RUNS_ENDPOINT

"""
SRC has had a long running issue (documented as early as March of 2019) where
submitting runs on behalf of other players - a 500 response occurs every
time this request is made. To work around this, we make a mod note on each run that
states what the submitter's SRC username (or the guest name, if applicable).
Then, moderators will need to go in and manually copy-paste this value into the runner
field to update to the correct value.

Check on the status of this issue at:
https://github.com/speedruncomorg/api/issues/87
"""

# Workaround currently defaulted to True until #87 is resolved
def move_runs(source_category_id, target_category_id, api_key_path, workaround_is_active=True):
    try:
        api_key = get_api_key(api_key_path)

        # Get runs and copy them to be POSTed to new location
        print("API key loaded successfully.")
        print("Getting source leaderboard runs from Speedrun.com ...\n")

        current_board_runs = retrieve_target_runs(source_category_id)

        print("Runs successfully acquired.")
        print("Generating new run submissions based on existing runs ...\n")

        generated_submissions = generate_run_request_data(current_board_runs, target_category_id, workaround_is_active)

        print("Run submissions generated.")

        # Start posting them to a new board
        print("Posting generated submissions ...\n")

        post_formatted_runs(generated_submissions, RUNS_ENDPOINT, api_key)

        print("Runs successfully posted. Leaderboard copying complete.")
        
    except Exception as ex:
        print("Error migrating runs. The following exception occurred:")
        print(ex)
    
