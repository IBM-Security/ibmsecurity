import ibmsecurity.utilities.tools

module_uri = "/isam/felb/configuration/ssl"
required_module = None  # TODO find out
required_version = None  # TODO find out


def add(isamAppliance, keyfile, check_mode=False, force=False):
    """
    Creates ssl configuration
    """
    if force is True or _check_add(isamAppliance, keyfile) is True:
        return isamAppliance.invoke_post("Creating Configuration", "{0}".format(module_uri),
                                         {
                                             "keyfile": keyfile
                                         }, requires_version=required_version, requires_modules=required_module)
    if check_mode is True:
        if _check_add(isamAppliance, keyfile) is False:
            return isamAppliance.create_return_object(changed=False)


def delete(isamAppliance, check_mode=False, force=False):
    """
    Deletes ssl configuration
    """
    return isamAppliance.invoke_delete("Disabling Configuration", "{0}".format(module_uri))


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieves ssl configuration
    """
    return isamAppliance.invoke_get("Retrieving Configuration", "{0}/".format(module_uri))


def update(isamAppliance, keyfile, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout, check_mode=False, force=False):
    """
    Updates keyfile
    """
    update_required = _check(isamAppliance, keyfile, is_primary, interface, remote, port, health_check_interval,
                             health_check_timeout)

    if update_required is True or force is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updated SSL configurations", module_uri,
                                            {
                                                "keyfile": keyfile,
                                                "is_primary": is_primary,
                                                "interface": interface,
                                                "remote": remote,
                                                "port": port,
                                                "health_check_interval": health_check_interval,
                                                "health_check_timeout": health_check_timeout

                                            }, requires_modules=required_module, requires_version=required_version)


def _check(isamAppliance, keyfile, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout):
    """
    Idempotency Test
    parameters past keyfile are set to none because create method uses only keyfile as parameter, functions main
    purpose is to check upon update.
    """
    ret_obj = get(isamAppliance)

    # Checks to see if parameters passed match values in original appliance
    if ret_obj['data']['keyfile'] != keyfile:
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


def _check_add(isamAppliance, keyfile):
    """
    checks add function for idempotency
    """
    change_required = False
    temp_obj = get(isamAppliance)
    if temp_obj['data']['enabled'] == True:
        if temp_obj['data']['keyfile'] != keyfile:
            change_required = True
            return change_required
    else:
        return change_required
