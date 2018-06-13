import ibmsecurity.utilities.tools

module_uri = "/isam/felb/configuration/ha"
requires_module = None
requires_version = None




def delete(isamAppliance, check_mode=False, force=False):
    """
    Disables High Availability Configuration
    """
    return isamAppliance.invoke_delete("Disabling High Availability", "{0}".format(module_uri))


def add(isamAppliance, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout, check_mode=False, force=False):
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
                                     }, requires_version=requires_version, requires_modules=requires_module)


def get(isamAppliance, check_mode=False, force=False):
    """
    Receives configuration
    """
    return isamAppliance.invoke_get("Receiving Configuration", "{0}".format(module_uri))


def update(isamAppliance, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout, check_mode=False, force=False):

    update_required = _check(isamAppliance, is_primary=is_primary, interface=interface, remote=remote,
                                        port=port, health_check_interval=health_check_interval,
                                        health_check_timeout=health_check_timeout)
    if force is True or update_required is True:
        return isamAppliance.invoke_put("Updating High Availability", module_uri,
                                            {
                                                "is_primary": is_primary,
                                                "interface": interface,
                                                "remote": remote,
                                                "port": port,
                                                "health_check_interval": health_check_interval,
                                                "health_check_timeout": health_check_timeout

                                            }, requires_modules=requires_module, requires_version=requires_version)
    elif check_mode is True:
        return isamAppliance.create_return_object(changed=False)




def _check(isamAppliance, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout, check_mode=False, force=False):
    """
    idempotency test for each parameter
    """
    ret_obj = get(isamAppliance)
    if ret_obj['data']['enabled'] != True:
        return True
    elif ret_obj['data']['is_primary'] != is_primary:
        return True
    elif ret_obj['data']['interface'] != interface:
        return True
    elif ret_obj['data']['remote'] != remote:
        return True
    elif ret_obj['data']['port'] != port:
        return True
    elif ret_obj['data']['health_check_interval'] != health_check_interval:
        return True
    elif ret_obj['data']['health_check_timeout'] != health_check_timeout:
        return True
    else:
        return False