def extract_times(raw_times_dict):
    """
    Extract the actual time values from the data provided by the SRC Run API.
    """
    actual_times = {}
    if raw_times_dict["realtime"] is not None:
        actual_times["realtime"] = raw_times_dict["realtime_t"]

    if raw_times_dict["realtime_noloads"] is not None:
        actual_times["realtime_noloads"] = raw_times_dict["realtime_noloads_t"]

    if raw_times_dict["ingame"] is not None:
        actual_times["ingame"] = raw_times_dict["ingame_t"]

    return actual_times


def format_run_for_post(run, variables=None):
    player_data = {
        "rel": run["players"][0]["rel"],
    }
    if player_data["rel"] == "user":
        player_data["id"] = run["players"][0]["id"]
    else:
        player_data["name"] = run["players"][0]["name"]

    post_data = {
        "run": {
            "category": run["category"],
            "date": run["date"],
            "region": run["system"]["region"],
            "platform": run["system"]["platform"],
            "verified": False,
            "times": {
                "realtime": run["times"]["primary_t"],
                "realtime_noloads": run["times"]["realtime_noloads_t"],
                "ingame": run.get("times", {}).get("ingame_t", 0)
            },
            "players": [player_data],
            "emulated": run["system"]["emulated"],
            "comment": run.get("comment", None),
        }
    }

    # Handle optional fields
    if run["level"] is not None:
        post_data["run"]["level"] = run["level"]

    if run.get("videos", None):
        post_data["run"]["video"] = run["videos"]["links"][0]["uri"]

    if run.get("splits", None):
        post_data["run"]["splitsio"] = run["splits"]["uri"].split("/")[-1]

    if variables:
        post_data["run"]["variables"] = variables

    return post_data
