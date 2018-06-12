import ibmsecurity.utilities.tools

module_uri = "/isam/felb/configuration/ssl"
required_module = None  # TODO find out
required_version = None  # TODO find out


def create(isamAppliance, keyfile, check_mode=False, force=False):
    """
    Creates ssl configuration
    """
    if check_mode is True or force is False:
        if _check(isamAppliance, keyfile) is True:
            return isamAppliance.create_return_object(changed=False)
        else:
            return isamAppliance.invoke_post("Creating Configuration", "{0}".format(module_uri),
                                             {
                                                 "keyfile": keyfile
                                             }, requires_version=required_version, requires_modules=required_module)


def disable(isamAppliance, check_mode=False, force=False):
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
    update_required, json_data = _check(isamAppliance, keyfile, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout)

    if update_required is True or force is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updated SSL configurations", module_uri, json_data, requires_modules=required_module, requires_version=required_version)


def _check(isamAppliance, keyfile, is_primary=None, interface=None, remote=None, port=None, health_check_interval=None,
           health_check_timeout=None):
    """
    Idempotency Test
    parameters past keyfile are set to none because create method uses only keyfile as parameter, functions main
    purpose is to check upon update.
    """
    update_required=False
    ret_obj = get(isamAppliance)

    json_data = {
        "keyfile": keyfile,
        "is_primary": is_primary,
        "interface": interface,
        "remote": remote,
        "port": port,
        "health_check_interval": health_check_interval,
        "health_check_timeout": health_check_timeout
        }
    #sorts data for comparing attributes
    sort_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
    sort_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj)

    if sort_json_data != sort_ret_obj:
        update_required=True

    return update_required, json_data
