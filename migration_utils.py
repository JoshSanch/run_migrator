import credentials_loader
import requests

from typing import Dict

RUNS_ENDPOINT = "https://www.speedrun.com/api/v1/runs"
CATEGORIES_ENDPOINT = "https://www.speedrun.com/api/v1/categories"

def get_target_runs(category_id):
    """
    Get all of the runs contained within an SRC leaderboard category as
    defined by the category's global ID. This ID is unique across all of SRC.
    """
    # Setup HTTP request data to get runs for category
    request_url = RUNS_ENDPOINT
    request_params = {
        "category": category_id,
        "status": "verified"
    }

    # Request and extract leaderboard data for given category
    response = requests.get(url=request_url, params=request_params)
    leaderboard_data =  response.json()["data"]
    return leaderboard_data

def post_runs(existing_runs: Dict):
    # Data params needed can be found at https://github.com/speedruncomorg/api/blob/master/version1/runs.md#post-runs
    for run in existing_runs:
        pass