import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isdsAppliance, check_mode=False, force=False):
    """
    Retrieving all interfaces
    :rtype: (str, dict)
    """
    return isdsAppliance.invoke_get("Retrieving all interfaces", "/widgets/mgmtinterface")

def get_all_app(isdsAppliance, check_mode=False, force=False):
    """
    Retrieving all application interfaces
    :rtype: (str, dict)
    """
    return isdsAppliance.invoke_get("Retrieving all application interfaces", "/application_interfaces")


def get(isdsAppliance, uuid, check_mode=False, force=False):
    """
    Retrieving a single interface
    """
    return isdsAppliance.invoke_get("Retrieving a single interface", "/application_interfaces/" + uuid + "/addresses/1")


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare interfaces between 2 appliances
    """
    ret_obj1 = get_all(isdsAppliance1)
    ret_obj2 = get_all(isdsAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
