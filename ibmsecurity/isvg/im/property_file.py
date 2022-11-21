import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/v1/property/propertyfiles"


def get_all(isvgAppliance, check_mode=False, force=False):
    """
    Retrieve a list of property files
    """
    return isvgAppliance.invoke_get("Retrieve a list of property files", uri)


def _get(isvgAppliance, propertyFile):
    return isvgAppliance.invoke_get("Retrieve properties for a specific file", "{0}/{1}".format(uri, propertyFile))


def search(isvgAppliance, propertyFile, check_mode=False, force=False):
    """
    Search property file by name
    """
    ret_obj = get_all(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['PropertyFile'] == propertyFile:
            logger.info("Found property file {0} type: {1}".format(propertyFile, obj['type']))
            return_obj['data'] = obj['PropertyFile']
            return_obj['rc'] = 0

    return return_obj
