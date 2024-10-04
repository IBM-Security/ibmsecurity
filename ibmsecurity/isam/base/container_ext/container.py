import logging

logger = logging.getLogger(__name__)

uri = "/isam/container_ext/container"

requires_version = "10.0.7.0"
requires_model = "Appliance"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all known deployment properties for managed containers
    """
    return isamAppliance.invoke_get("Retrieving managed container properties",
                                    "{0}".format(uri),
                                    requires_model=requires_model, requires_version=requires_version)



