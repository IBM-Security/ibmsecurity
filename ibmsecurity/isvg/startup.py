import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/startup"

def get(isvgAppliance, check_mode=False, force=False):
    """
    Get Identity Manager data stores status
    """
    return isvgAppliance.invoke_get("Retrieving startup configuration status", uri)
