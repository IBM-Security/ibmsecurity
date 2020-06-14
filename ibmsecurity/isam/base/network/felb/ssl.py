import ibmsecurity.utilities.tools
import logging

module_uri = "/isam/felb/configuration/ssl"
requires_module = None
requires_version = None
requires_model = "Appliance"

logger = logging.getLogger(__name__)


def enable(isamAppliance, keyfile, check_mode=False, force=False):
    """
    Creating SSL configuration
    """

    check_enable, warnings = _check_enable(isamAppliance, keyfile)
    if force is True or check_enable is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post("Creating SSL configuration", module_uri,
                                             {
                                                 "keyfile": keyfile
                                             },
                                             requires_version=requires_version,
                                             requires_modules=requires_module,
                                             requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def disable(isamAppliance, check_mode=False, force=False):
    """
    Deletes ssl configuration
    """

    check_disable, warnings = _check_disable(isamAppliance)
    if force is True or check_disable is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete("Disabling SSL", module_uri,
                                               requires_version=requires_version,
                                               requires_modules=requires_module,
                                               requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieves ssl configuration
    """
    return isamAppliance.invoke_get("Retrieving SSL configuration", module_uri,
                                    requires_version=requires_version,
                                    requires_modules=requires_module,
                                    requires_model=requires_model)


def update(isamAppliance, keyfile, check_mode=False, force=False):
    """
    Updating SSL configuration
    """
    # Call to check function to see if configuration already exist
    update_required, warnings = _check_enable(isamAppliance, keyfile)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Updating SSL configuration", module_uri,
                                            {
                                                'keyfile': keyfile

                                            },
                                            requires_modules=requires_module,
                                            requires_version=requires_version,
                                            requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_enable(isamAppliance, keyfile=None):
    """
    checks add function for idempotency
    """
    change_required = False
    check_obj = get(isamAppliance)
    warnings = check_obj['warnings']
    # checks to see if ssl configuration exists

    if 'enabled' in check_obj['data']:
        if check_obj['data']['enabled'] is False:
            return True, warnings
        elif check_obj['data']['keyfile'] != keyfile:
            return True, warnings
        else:
            return False, warnings
    else:
        return False, warnings


def _check_disable(isamAppliance):
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
        return False, warnings


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
