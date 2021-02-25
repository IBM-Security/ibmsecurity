import logging

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/apiac/groups"
requires_modules = ["wga"]
requires_version = "9.0.7"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of all ISAM groups
    """
    return isamAppliance.invoke_get("Retrieve a list of all ISAM groups",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)
