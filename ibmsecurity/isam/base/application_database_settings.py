import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/core/update_servers"
requires_modules = None
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get Update Servers
    """
    return isamAppliance.invoke_post("Get Update Servers", uri, requires_modules=requires_modules,
                                        requires_version=requires_version)
