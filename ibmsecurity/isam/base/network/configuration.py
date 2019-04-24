import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/net"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the network configuration
    """
    return isamAppliance.invoke_get("Retrieving the network configuration", uri)
