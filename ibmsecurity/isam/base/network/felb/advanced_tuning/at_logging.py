import ibmsecurity.utilities.tools
import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/logging"
requires_modules = None
requires_versions = None


def get(isamAppliance):
    """
    Retrieves logging configuration attributes
    """
    return isamAppliance.invoke_get("Retrieving logging configuration attributes", module_uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_versions)


def update(isamAppliance, local, remote_address, remote_port, remote_facility, check_mode=False, force=False):
    """
    Updates logging configuration
    """
    change_required, json_data = _check_update(isamAppliance, local, remote_address, remote_port, remote_facility)

    if force is True or change_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating logging configuration attributes", module_uri, json_data,
                                            requires_modules=requires_modules, requires_version=requires_versions)

    else:
        return isamAppliance.create_return_object()


def _check_update(isamAppliance, local, remote_address, remote_port, remote_facility):
    """
    Checks update for idempotency
    """
    change_required = False
    check_obj = get(isamAppliance)

    # checks to see if logging is local or remote, if remote all other data gets set to None
    if check_obj['data']['local'] is True:
        if check_obj['data']['local'] != local:
            change_required = True

        json_data = {
            "local": True,
            "remote_address": None,
            "remote_port": None,
            "remote_facility": None
        }

    else:
        json_data = {
            "local": local,
            "remote_address": remote_address,
            "remote_port": remote_port,
            "remote_facility": remote_facility
        }
        if check_obj['data']['local'] != local:
            change_required = True
            return change_required, json_data
        if check_obj['data']['remote_address'] != remote_address:
            change_required = True
            return change_required, json_data
        if check_obj['data']['remote_port'] != remote_port:
            change_required = True
            return change_required, json_data
        if check_obj['data']['remote_facility'] != remote_facility:
            change_required = True
            return change_required, json_data

        else:
            return change_required, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
