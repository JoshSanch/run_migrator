import json
import requests

from .src_conversion_utils import extract_times
from api.scoping import Scope
from typing import Dict

RUNS_ENDPOINT = "https://www.speedrun.com/api/v1/runs"
CATEGORIES_ENDPOINT = "https://www.speedrun.com/api/v1/categories"

def retrieve_target_runs(source_id, scope) -> list:
    """
    Get all of the runs contained within an SRC leaderboard category as
    defined by the category's global ID. This ID is unique across all of SRC.
    """
    # Setup HTTP request data to get runs for category
    request_url = RUNS_ENDPOINT
    request_params = {
        "status": "verified"
    }

    # Modify request depending on if we want to query a category or a whole game
    if scope == Scope.CategoryScope:
        request_params["category"] = source_id
    elif scope == Scope.GameScope:
        request_params["game"] = source_id

    # Request and extract leaderboard data for given category
    response = requests.get(url=request_url, params=request_params)
    response.raise_for_status()

    leaderboard_data = []
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

def generate_run_request_data(existing_runs, target_category_id: str, workaround_active):
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

        if not workaround_active:
            # Don't verify so that runs can be manually updated by mods
            # to have the correct submitting user
            request_body["verified"] = True

        request_body["times"] = extract_times(run["times"])
        comment = ""  # Start robust comment handling for workaround
        
        # SRC is a good platform
        # See run_mover.py for an explanation of why this is needed
        if not workaround_active:
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
            comment += run["comment"]
        
        if "system" in run:
            if "platform" in run["system"]:  # Not actually optional
                request_body["platform"] = run["system"]["platform"]

            if "emulated" in run["system"]:
                request_body["emulated"] = run["system"]["emulated"]

            if "region" in run["system"]:
                request_body["region"] = run["system"]["region"]

        if "videos" in run and run["videos"] is not None:
            request_body["video"] = run["videos"]["links"][0]["uri"]

        # Handle SRC 500 error workaround - see run_mover.py for details
        if workaround_active:
            if comment:  # Append to existing comment
                comment += f"\nMod note: Submitted by {retrieve_submitter_name(run)}"
            else:
                comment = f"Mod note: Submitted by {retrieve_submitter_name(run)}"

        # Finalize comment to append
        request_body["comment"] = comment

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

def retrieve_submitter_name(run):
    run_player_data = run["players"][0]  # Assume this tool will only work for one-player runs
    if run_player_data["rel"] == "guest":
        # Simple - submitter name is hardcoded into run data
        return run_player_data["name"]

    # Perform get request on user ID to get user data for name extraction
    request_url = run_player_data["uri"]  # "rel" has to be "user" if they're not a guest, meaning api returns a user url
    response = requests.get(url=request_url)
    
    # Extract name data
    user_data = response.json()["data"]
    name = user_data["names"]["international"]
    return name
