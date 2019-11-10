import credentials_loader
import json
import requests

from src_conversion_utils import extract_times
from typing import Dict

RUNS_ENDPOINT = "https://www.speedrun.com/api/v1/runs"
CATEGORIES_ENDPOINT = "https://www.speedrun.com/api/v1/categories"

def get_target_runs(category_id):
    """
    Get all of the runs contained within an SRC leaderboard category as
    defined by the category's global ID. This ID is unique across all of SRC.
    """
    # Setup HTTP request data to get runs for category
    # TODO: Handle pagination issues where I only get 20 results
    request_url = RUNS_ENDPOINT
    request_params = {
        "category": category_id,
        "status": "verified"
    }

    # Setup intermediate dict for storing data
    leaderboard_data = []

    # Request and extract leaderboard data for given category
    response = requests.get(url=request_url, params=request_params)
    response.raise_for_status()

    for run in response.json()["data"]:
        leaderboard_data.append(run)

    # Handle pagination
    pagination_data = response.json()["pagination"]["links"]
    new_url = None
    for page_data in pagination_data:
        if page_data["rel"] == "next":
            new_url = page_data["uri"]

    # Start iterating through pages till we're done
    while new_url is not None:
        response = requests.get(url=new_url)
        response.raise_for_status()

        for run in response.json()["data"]:
            leaderboard_data.append(run)

        pagination_data = response.json()["pagination"]["links"]
        new_url = None
        for page_data in pagination_data:
            if page_data["rel"] == "next":
                new_url = page_data["uri"]
        
    return leaderboard_data

def generate_run_request_data(existing_runs, target_category_id: str):
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
        request_body["verified"] = True
        request_body["times"] = extract_times(run["times"])
        request_body["players"] = run["players"]  # ALWAYS HAVE THIS - OTHERWISE SRC DEFAULTS TO MAKING SUBMITTER THE RUNNER
        try:
            request_body["players"][0].pop("uri")
        except:
            print("no player url found")

        # Optional fields
        if "date" in run and run["date"] is not None:
            request_body["date"] = run["date"]

        if "splits" in run and run["splits"] is not None:
            request_body["splitsio"] = run["splits"]

        if "comment" in run and run["comment"] is not None:
            request_body["comment"] = run["comment"]
        
        if "system" in run:
            if "platform" in run["system"]:  # Not actually optional
                request_body["platform"] = run["system"]["platform"]

            if "emulated" in run["system"]:
                request_body["emulated"] = run["system"]["emulated"]

            if "region" in run["system"]:
                request_body["region"] = run["system"]["region"]

        if "videos" in run and run["videos"] is not None:
            request_body["video"] = run["videos"]["links"][0]["uri"]

        generated_runs.append(request_body)

    return generated_runs

def post_formatted_runs(runs, endpoint, api_key):
    """
    Runs going in here should represent the data format found
    at https://github.com/speedruncomorg/api/blob/master/version1/runs.md#post-runs.
    This will always be the case if raw API data is run through 
    generate_run_request_data.
    """
    for run in runs:
        data = {}
        data["run"] = run
        headers = {
            "Accept": "application/json",
            "X-API-Key": api_key
        }

        json_data = json.dumps(data)

        attempts = 0
        response = requests.post(url=RUNS_ENDPOINT, data=json_data, headers=headers)
        while(attempts < 3 and response.status_code != 201):
            attempts += 1
            response = requests.post(url=RUNS_ENDPOINT, data=json_data, headers=headers)

        if response.status_code != 201:
            print(f"Run with date {run['date']} failed to upload.")
            print(response.status_code)
        

def dump_runs(runs, target_file_path):
    with open(target_file_path, "w+") as dump_file:
        for run in runs:
            json.dump(run, dump_file, indent=4)
