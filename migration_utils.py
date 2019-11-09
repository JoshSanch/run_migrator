import credentials_loader
import json
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

def generate_run_request_data(existing_runs: Dict, target_category_id: str):
    """
    Populate all necessary POST data values as specified by the SRC
    documentation. Used as an intermediate state between either a POST
    request or a text file dump.
    """
    generated_runs = []

    # Data params needed can be found at https://github.com/speedruncomorg/api/blob/master/version1/runs.md#post-runs
    for run in existing_runs:
        request_body = {}
        request_body["category"] = target_category_id
        request_body["date"] = run["date"]
        request_body["verified"] = True,
        request_body["times"] = run["times"]
        request_body["players"] = run["players"]  # ALWAYS HAVE THIS - OTHERWISE SRC DEFAULTS TO MAKING SUBMITTER THE RUNNER
        request_body["comment"] = run["comment"]

        # Optional fields
        if "splits" in run:
            request_body["splitsio"] = run["splits"]

        if "comment" in run:
            request_body["comment"] = run["comment"]
        
        if "system" in run:
            if "platform" in run["system"]:
                request_body["platform"] = run["system"]["platform"]

            if "emulated" in run["system"]:
                request_body["emulated"] = run["system"]["emulated"]

            if "region" in run["system"]:
                request_body["region"] = run["system"]["region"]

        if "videos" in run and run["videos"] is not None:
            request_body["video"] = run["videos"]["links"][0]["uri"]

        generated_runs.append(request_body)

    return generated_runs

def dump_runs(runs, target_file_path):
    with open(target_file_path, "w+") as dump_file:
        for run in runs:
            json.dump(run, dump_file, indent=4)
