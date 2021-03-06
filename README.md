# run_migrator
Python API implementation for migrating runs between two category leaderboards on Speedrun.com.

**Note:** Currently there is a manual workaround necessary where submitting runs on behalf of another user 
returns a 500 error, even if you have sufficient permissions to execute the request (board moderator/super moderator, etc.).
The program can only currently submit runs to the target leaderboard that are unverified and will have a submission
user of the user that corresponds to the API key used to run this program.

Users will need to manually edit the submission user and then verify runs. To make this easier,
the program will add a mod note to each submission with the exact name of the user (or guest, should that case occur).

## Usage
```run_mover.py``` contains the top level method, ```move_runs```, which can be used to copy runs to another leaderboard
from a given source leaderboard. (**Note**: Until [this Github issue](https://github.com/speedruncomorg/api/issues/87) is resolved,
the workaround flag should be set to True to make sure the workaround behavior is applied.)

Parameter Descriptions:
```
source_category_id: The ID of the category that contains the source to be copied, as defined by the SRC API.
target_category_id: The ID of the category that runs should be copied to, as defined by the SRC API.
api_key_path: The path to the JSON file that contains the user's API key.
workaround_is_active: Defaults to true. Activates the workaround behavior necessary while the SRC 500 error is yet to be fixed.
```

## Contributing
Pull requests to add category & game IDs to expand the catalog of ready to use
IDs for scripting purposes are much appreciated.

Project requirements are contained within ```requirements.txt```.
