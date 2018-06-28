import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/logging"
requires_modules = None
requires_versions = None


def get(isamAppliance):
    """
    Retrieves logging configuration attributes
    """
    return isamAppliance.invoke_get("Retrieving logging configuration", module_uri)


def update(isamAppliance, local, remote_address, remote_port, remote_facility, check_mode=False, force=False):
    """
    Updates logging configuration
    """
    change_required, json_data = _check(isamAppliance, local, remote_address, remote_port, remote_facility)

    if force is True or change_required is True:
        return isamAppliance.invoke_put("Updating Configuration", module_uri, json_data,
                                        requires_modules=requires_modules, requires_version=requires_versions)
    if change_required is False:
        return isamAppliance.create_return_object(changed=False)


def _check(isamAppliance, local, remote_address, remote_port, remote_facility):
    """
    Check for idempotency
    """
    check_obj = get(isamAppliance)
    change_required = False
    # If the configuration is local, remote entries are not used
    if local is True:
        json_data = {
            "local": True,
            "remote_address": "",
            "remote_port": None,
            "remote_facility": None

        }
        if check_obj['data']['local'] != local:
            change_required = True
        return change_required, json_data
    else:
        if check_obj['data']['remote_address'] != remote_address:
            change_required = True
        if check_obj['data']['remote_port'] != remote_port:
            change_required = True
        if check_obj['data']['remote_facility'] != remote_facility:
            change_required = True

        json_data = {
            "local": local,
            "remote_address": remote_address,
            "remote_port": remote_port,
            "remote_facility": remote_facility
        }

        return change_required, json_data
