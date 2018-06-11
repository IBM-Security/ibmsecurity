import ibmsecurity.utilities.tools

module_uri = "/isam/felb/configuration/ha"
requires_module = None
requires_version = None




def disable(isamAppliance, check_mode=False, force=False):
    """
    Disables High Availability Configuration
    """
    return isamAppliance.invoke_delete("Disabling High Availability", "{0}".format(module_uri))


def enable(isamAppliance, is_primary=False, interface=None, remote=None, port=None, health_check_interval=None,
           health_check_timeout=None, check_mode=False, force=False):
    """
    enables HA
    """
    return isamAppliance.invoke_post("Enabling High Availability Configuration", "{0}".format(module_uri),
                                     {
                                         "is_primary": is_primary,
                                         "interface": interface,
                                         "remote": remote,
                                         "port": port,
                                         "health_check_interval": health_check_interval,
                                         "health_check_timeout": health_check_timeout
                                     })


def get(isamAppliance, check_mode=False, force=False):
    """
    Receives configuration
    """
    return isamAppliance.invoke_get("Receiving Configuration", "{0}".format(module_uri))


def update(isamAppliance, is_primary=False, interface=None, remote=None, port=None, health_check_interval=None,
           health_check_timeout=None, check_mode=False, force=False):

    update_required, json_data = _check(isamAppliance, is_primary=is_primary, interface=interface, remote=remote,
                                        port=port, health_check_interval=health_check_interval,
                                        health_check_timeout=health_check_timeout)
    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating High Availability", module_uri, json_data, requires_modules=requires_module, requires_version=requires_version)




def _check(isamAppliance, is_primary=False, interface=None, remote=None, port=None, health_check_interval=None,
           health_check_timeout=None, check_mode=False, force=False):
    """
    idempotency test for each parameter
    """
    ret_obj = get(isamAppliance)
    update_required = False

    json_data = {
        "is_primary": is_primary,
        "interface": interface,
        "remote": remote,
        "port": port,
        "health_check_interval": health_check_interval,
        "health_check_timeout": health_check_timeout
    }
    # sorting input and initial appliance data
    sort_json_data = ibmsecurity.utilities.tools.json_sort(json_data)

    sort_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj)

    if sort_ret_obj != sort_json_data:
        logger.info("changes needed")
        update_required = True

    return update_required, json_data
