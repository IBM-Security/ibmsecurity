import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/widgets/notifications"

def get(isvgAppliance, check_mode=False, force=False):
    """
    Get Identity Manager data stores status
    """
    return isvgAppliance.invoke_get("Retrieving notifications status", uri)
