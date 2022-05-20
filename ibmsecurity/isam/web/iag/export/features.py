import logging
import ibmsecurity.utilities.tools
import json

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/iag/export"
requires_modules = ["wga"]
requires_version = None

def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the administrator settings
    """
    return isamAppliance.invoke_get("Retrieving the administrator settings", uri+"/features")

#download
#list
#features






