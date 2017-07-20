import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/core/dca_updates_cfg"
requires_modules = None
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get Application Database Settings
    """
    return isamAppliance.invoke_post("Get Application Database Settings", uri, requires_modules=requires_modules,
                                        requires_version=requires_version)
