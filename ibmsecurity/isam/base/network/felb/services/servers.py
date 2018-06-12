import ibmsecurity.utilities.tools

module_uri = "/isam/felb/configuration/services/"
requires_modulers = None
requires_version = None


def create(isamAppliance, service_name, address, active, port, weight, secure, ssllabel, check_mode=False, force=False):
    """
    Creates server under specificed service name
    """
    change_required=False

    change_required, json_data = _check(isamAppliance, service_name, address, active, port, weight, secure, ssllabel)

    if force is True or change_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Creating Server", "{0}{1}/servers/{2}".format(module_uri, service_name, address), json_data)


def delete(isamAppliance, service_name, address, check_mode=False, force=False):
    """
    deletes a server from specified service name
    """
    return (isamAppliance.invoke_delete("Deleting Server", "{0}{1}/servers/{2}".format(module_uri, service_name, address)))


def get(isamAppliance, service_name, address, check_mode=False, force=False):
    """
    Retrieves server from specified service name
    """
    return (isamAppliance.invoke_get("Deleting Server", "{0}{1}/servers/{2}".format(module_uri, service_name, address)))

def get_servers(isamAppliance, service_name, check_mode=False, force=False):
    """
    Retrieves a list of servers under a specified service
    """
    return isamAppliance.invoke_get("Retrieving Servers", "{0}{1}/servers".format(module_uri, service_name))


def update(isamAppliance, service_name, address, active, port, weight, secure=False, ssllabel=None, check_mode=False, force=False):
    """
    Updating server
    """

    change_required = False

    change_required, json_data = _check(isamAppliance, service_name, address, active, port, weight, secure, ssllabel)

    if force is True or change_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Updating Server",
                                             "{0}{1}/servers/{2}".format(module_uri, service_name, address), json_data)

def _check(isamAppliance, service_name, address, active, port, weight, secure=False, ssllabel=None):
    """
    idempontency test
    """
    change_required=False
    try:
        org_obj = get(isamAppliance, service_name, address)
        json_data = {
            "active": active,
            "address": address,
            "port": port,
            "weight": weight,
            "secure": secure,
            "ssllabel": ssllabel
        }
    except:
        change_required=True
        return change_required, json_data

    sort_org_obj= ibmsecurity.utilities.tools.json_sort(org_obj)
    sort_json_data= ibmsecurity.utilities.tools.json_sort(json_data)

    if sort_json_data != sort_org_obj:
        change_required=True

    return change_required, json_data