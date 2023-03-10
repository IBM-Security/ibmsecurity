import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/widgets/apphealth"

def get(isvgAppliance, check_mode=False, force=False):
    """
    Get Identity Manager data stores status
    """
    return isvgAppliance.invoke_get("Retrieving Identity Manager data stores status", uri)
