import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/logging"
requires_modules = None
requires_versions = None
requires_model="Appliance"


def get(isamAppliance):
    """
    Retrieving logging configuration attributes
    """
    return isamAppliance.invoke_get("Retrieving logging configuration attributes", module_uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_versions,
                                    requires_model=requires_model)


def update(isamAppliance, local, remote_address, remote_port, remote_facility, check_mode=False, force=False):
    """
    Updates logging configuration
    """
    json_data = {
        "local": local,
        "remote_address": remote_address,
        "remote_port": remote_port,
        "remote_facility": remote_facility
    }

    change_required, warnings = _check(isamAppliance, json_data)

    if force is True or change_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Updating logging configuration attributes", module_uri, json_data,
                                            requires_modules=requires_modules,
                                            requires_version=requires_versions,
                                            requires_model=requires_model)

    else:
        return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, json_data):
    """
    Checks update for idempotency
    """
    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']
    change_required = False

    if json_data['local'] is True:
        if 'local' in ret_obj['data']:
            if json_data['local'] != ret_obj['data']['local']:
                change_required = True
    else:
        sorted_ret_obj = tools.json_sort(ret_obj['data'])
        sorted_json_data = tools.json_sort(json_data)

        logger.debug(f"Sorted Existing Data:{sorted_ret_obj}")
        logger.debug(f"Sorted Desired  Data:{sorted_json_data}")

        if sorted_ret_obj != sorted_json_data:
            change_required = True

    return change_required, warnings


def compare(isamAppliance1, isamAppliance2):
    """
    Compare configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
