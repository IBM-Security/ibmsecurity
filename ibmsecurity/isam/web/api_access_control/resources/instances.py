import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/apiac/resource/instance"
requires_modules = ["wga"]
requires_version = "9.0.7"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of all Reverse Proxy Instances
    """
    return isamAppliance.invoke_get("Retrieve a list of all Reverse Proxy Instances",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, instance_name, check_mode=False, force=False):
    """
    Retrieve a single Reverse Proxy Instance
    """
    return isamAppliance.invoke_get("Retrieve a single Reverse Proxy Instance",
                                    "{0}/{1}".format(uri, instance_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare resources between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2)
