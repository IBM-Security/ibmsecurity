import ibmsecurity.utilities.tools
import logging

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/ha"
requires_modules = None
requires_version = None
requires_model = "Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving HA configuration
    """
    return isamAppliance.invoke_get("Retrieving HA configuration", module_uri,
                                    requires_version=requires_version, requires_modules=requires_modules,
                                    requires_model=requires_model)


def disable(isamAppliance, check_mode=False, force=False):
    """
    Disabling HA
    """

    check_value, warnings = _check_enable(isamAppliance)

    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete("Disabling HA", module_uri,
                                               requires_version=requires_version,
                                               requires_modules=requires_modules,
                                               requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def enable(isamAppliance, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout, check_mode=False, force=False):
    """
    Enabling HA
    """

    json_data = {
        "is_primary": is_primary,
        "interface": interface,
        "remote": remote,
        "port": port,
        "health_check_interval": health_check_interval,
        "health_check_timeout": health_check_timeout
    }

    check_value, warnings = _check_enable(isamAppliance)

    if force is True or check_value is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post("Enabling HA", module_uri,
                                             json_data,
                                             requires_version=requires_version,
                                             requires_modules=requires_modules,
                                             requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout, check_mode=False, force=False):
    """
    Updating HA configuration
    """

    json_data = {
        "is_primary": is_primary,
        "interface": interface,
        "remote": remote,
        "port": port,
        "health_check_interval": health_check_interval,
        "health_check_timeout": health_check_timeout
    }

    # Call to check function to see if configuration already exist
    update_required, warnings = _check_update(isamAppliance, json_data)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnigns=warnings)
        else:
            return isamAppliance.invoke_put("Updating HA configuration", module_uri,
                                            json_data,
                                            requires_modules=requires_modules,
                                            requires_version=requires_version,
                                            requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, is_primary, interface, remote, port, health_check_interval,
        health_check_timeout, check_mode=False, force=False):
    """
    determines if add or update is used.
    """

    is_enabled, warnings = _check_enable(isamAppliance)


    if is_enabled is False:
        return enable(isamAppliance, is_primary=is_primary, interface=interface, remote=remote, port=port,
                      health_check_interval=health_check_interval,
                      health_check_timeout=health_check_timeout, check_mode=check_mode, force=force)
    elif is_enabled is True:
        return update(isamAppliance, is_primary=is_primary, interface=interface, remote=remote, port=port,
                      health_check_interval=health_check_interval,
                      health_check_timeout=health_check_timeout, check_mode=check_mode, force=force)
    else:
        return isamAppliance.create_return_object(warnings=warnings)

def _check_update(isamAppliance, json_data):
    """
    idempotency test for each parameter
    """

    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']

    if 'enabled' in ret_obj['data']:
        if ret_obj['data']['enabled'] is False:
            return False, warnings
        else:
            del ret_obj['data']['enabled']

    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(json_data)
    logger.debug(f"Sorted Existing Data:{sorted_ret_obj}")
    logger.debug(f"Sorted Desired  Data:{sorted_json_data}")
    if sorted_ret_obj != sorted_json_data:
        return True, warnings
    else:
        return False, warnings


def _check_enable(isamAppliance):
    """
    Checks delete function for idempotency
    """

    check_obj = get(isamAppliance)
    warnings = check_obj['warnings']

    if 'enabled' in check_obj['data']:
        if check_obj['data']['enabled'] == True:
            return True, warnings
        else:
            return False, warnings
    else:
        return None, warnings


def compare(isamAppliance1, isamAppliance2):
    """
    Compare FELB HA configuration between two appliances
    """

    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
