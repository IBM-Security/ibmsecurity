import logging

logger = logging.getLogger(__name__)
uri = "/sys"
requires_model = "Appliance"


def get_routes(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current active system routes
    """
    return isamAppliance.invoke_get("Retrieving the current active system routes", "{}/routes".format(uri),
                                    requires_model=requires_model)


def get_addresses(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the currently assigned addresses
    """
    return isamAppliance.invoke_get("Retrieving the currently assigned addresses", "{}/ifaces".format(uri),
                                    requires_model=requires_model)
