import ibmsecurity.utilities.tools

module_uri = "/isam/felb/configuration/services/"
requires_modulers = None
requires_version = None


def add(isamAppliance, service_name, address, active, port, weight, secure, ssllabel, check_mode=False, force=False):
    """
    Creates server under specificed service name
    """
    change_required = _check(isamAppliance, service_name, address, active, port, weight, secure, ssllabel)

    if force is True or change_required is True:
        return isamAppliance.invoke_post("Creating Server", "{0}{1}/servers".format(module_uri, service_name, address),
                                         {
                                             "active": active,
                                             "address": address,
                                             "port": port,
                                             "weight": weight,
                                             "secure": secure,
                                             "ssllabel": ssllabel

                                         },
                                         requires_version=requires_version, requires_modules=requires_modulers)
    else:
        return isamAppliance.create_return_object(changed=False)


def delete(isamAppliance, service_name, address, check_mode=False, force=False):
    """
    deletes a server from specified service name
    """
    return (
        isamAppliance.invoke_delete("Deleting Server", "{0}{1}/servers/{2}".format(module_uri, service_name, address)))


def get(isamAppliance, service_name, address, check_mode=False, force=False):
    """
    Retrieves server from specified service name
    """
    return (
        isamAppliance.invoke_get("Retrieving Server", "{0}{1}/servers/{2}".format(module_uri, service_name, address)))


def get_all(isamAppliance, service_name, check_mode=False, force=False):
    """
    Retrieves a list of servers under a specified service
    """
    return isamAppliance.invoke_get("Retrieving Servers", "{0}{1}/servers".format(module_uri, service_name))


def update(isamAppliance, service_name, address, active, port, weight, secure=False, ssllabel=None, new_address=None, new_port=None, check_mode=False,
           force=False):
    """
    Updating server
    """
    # TODO ask why this keeps adding port to address

    change_required = _check(isamAppliance, service_name, address, active, port, weight, secure, ssllabel, new_address, new_port)

    json_data = {
        "active": active,
        "weight": weight,
        "secure": secure,
        "ssllabel": ssllabel
    }
    if new_address is not None:
        json_data["address"] = new_address
    else:
        json_data["address"]= address
    if new_port is not None:
        json_data["port"] = new_port
    else:
        json_data["port"] = port

    if force is True or change_required is True:
        isamAppliance.invoke_put("Updating Server",
                                 "{0}{1}/servers/{2}".format(module_uri, service_name, "{0}:{1}".format(address, port)), json_data,
                                 requires_modules=requires_modulers, requires_version=requires_version)
    else:
        return isamAppliance.create_return_object(changed=False)


def _check(isamAppliance, service_name, address, active, port, weight, secure=False, ssllabel=None, new_address=None, new_port=None):
    """
    idempontency test
    """
    change_required = False

    org_obj = get(isamAppliance, service_name, "{0}:{1}".format(address, port))
    if new_address or new_port is not None: #check to change address or port number
        change_required=True
        return change_required
    if org_obj['data']['address'] != address:
        change_required = True
        return change_required
    elif org_obj['data']['active'] != active:
        change_required = True
        return change_required
    elif org_obj['data']['port'] != port:
        change_required = True
        return change_required
    elif org_obj['data']['weight'] != weight:
        change_required = True
        return change_required
    elif org_obj['data']['secure'] != secure:
        change_required = True
        return change_required
    elif org_obj['data']['ssllabel'] != ssllabel:
        change_required = True
        return change_required
    else:
        return change_required
