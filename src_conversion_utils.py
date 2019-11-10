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