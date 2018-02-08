import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve current version.
    """
    return isamAppliance.invoke_get("Retrieving version",
                                    "/core/sys/versions")
