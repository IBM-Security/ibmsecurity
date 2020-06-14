import ibmsecurity.utilities.tools
import logging

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/services"
requires_modules = None
requires_version = None
requires_model = "Appliance"


def get(isamAppliance, service_name, check_mode=False, force=False):
    """
    Retrieving Layer Configuration
    """
    return isamAppliance.invoke_get("Retrieving Layer Configuration", "{0}/{1}/layer".format(module_uri, service_name),
                                    requires_version=requires_version, requires_modules=requires_modules,
                                    requires_model=requires_model)


def update(isamAppliance, service_name, type, layer7_secure, layer7_ssl_label, layer7_cookie, check_mode=False,
           force=False):
    """
    Updates specified service name layer
    """

    json_data = {'type': type}
    if type == "layer7":
        json_data['layer7_secure'] = layer7_secure
        json_data['layer7_cookie'] = layer7_cookie
        json_data['layer7_ssl_label'] = layer7_ssl_label

    change_required, warnings = _check(isamAppliance, service_name, json_data)

    if force is True or change_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Updating Service Layer", "{0}/{1}/layer".format(module_uri, service_name),
                                            json_data, requires_version=requires_version,
                                            requires_modules=requires_modules, requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, service_name, json_data):
    """
    Checks update for idempotency
    """

    ret_obj = get(isamAppliance, service_name)
    warnings = ret_obj['warnings']

    if ret_obj['data'] == {}:
        return False, warnings

    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(json_data)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))

    if sorted_ret_obj != sorted_json_data:
        return True, warnings
    else:
        return False, warnings


def compare(isamAppliance1, service_name1, isamAppliance2, service_name2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1, service_name1)
    ret_obj2 = get(isamAppliance2, service_name2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
