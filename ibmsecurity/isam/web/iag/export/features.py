import logging
import ibmsecurity.utilities.tools
import json

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/iag/export/features"
requires_modules = ["wga"]
requires_version = None

def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the wga features for iag
    """
    return isamAppliance.invoke_get("Retrieving the administrator settings", uri)

#download
#list
#features






