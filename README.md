# run_migrator
Python scripts for migrating runs between two category leaderboards on Speedrun.com.

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
