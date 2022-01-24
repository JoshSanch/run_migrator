import json
import requests
from utils.endpoints import CATEGORIES_ENDPOINT, GAME_ENDPOINT, LEVELS_ENDPOINT
from api.scoping import Scope


def fetch_variables(source_id: str, scope: Scope):
    """
    Get the variables for the resource with the given
    source id. The scope should be used to determine what
    type of resource is being fetched.
    """
    scope_endpt_map = {
        scope.CategoryScope: CATEGORIES_ENDPOINT,
        scope.LevelScope: LEVELS_ENDPOINT,
        scope.GameScope: GAME_ENDPOINT,
    }

    endpoint = scope_endpt_map[scope] + f"/{source_id}/variables"
    response = requests.get(endpoint)
    response.raise_for_status()

    return json.loads(response.content)
