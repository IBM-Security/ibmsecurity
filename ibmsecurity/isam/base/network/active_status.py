import logging

logger = logging.getLogger(__name__)
uri = "/sys"


def get_routes(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current active system routes
    """
    return isamAppliance.invoke_get("Retrieving the current active system routes", "{}/routes".format(uri))


def get_addresses(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the currently assigned addresses
    """
    return isamAppliance.invoke_get("Retrieving the currently assigned addresses", "{}/ifaces".format(uri))
