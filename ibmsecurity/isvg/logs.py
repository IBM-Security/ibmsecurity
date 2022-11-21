import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_event_log(isvgAppliance, check_mode=False, force=False):
    """
    Get Event Log
    """
    return isvgAppliance.invoke_get("Retrieving Event Log", "/events/system")
