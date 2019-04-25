import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isdsAppliance, check_mode=False, force=False):
    """
    Get Event Log
    """
    return isdsAppliance.invoke_get("Retrieving Authentication Token", "/authenticate")
