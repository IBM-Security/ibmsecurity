import ibmsecurity.utilities.tools
import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/services/"
requires_modulers = None
requires_version = None


def add(isamAppliance, service_name, address, active, port, weight, secure, ssllabel, check_mode=False, force=False):
    """
    Creating a server
    """
    change_required = _check_exist(isamAppliance, service_name, address, port=port)

    if force is True or change_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_post("Creating a server",
                                             "{0}{1}/servers".format(module_uri, service_name, address),
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
        return isamAppliance.create_return_object()


def delete(isamAppliance, service_name, address, check_mode=False, force=False):
    """
    deletes a server from specified service name
    """
    if force is True or _check_exist(isamAppliance, service_name, address) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting a server",
                                               "{0}{1}/servers/{2}".format(module_uri, service_name, address),
                                               requires_version=requires_version, requires_modules=requires_modulers)

    else:
        return isamAppliance.create_return_object()


def get(isamAppliance, service_name, address, check_mode=False, force=False):
    """
    Retrieves server from specified service name
    """
    return (
        isamAppliance.invoke_get("Retrieving a server", "{0}{1}/servers/{2}".format(module_uri, service_name, address),
                                 requires_version=requires_version, requires_modules=requires_modulers))


def get_all(isamAppliance, service_name, check_mode=False, force=False):
    """
    Retrieves a list of servers under a specified service
    """
    return isamAppliance.invoke_get("Retrieving servers for a service",
                                    "{0}{1}/servers".format(module_uri, service_name),
                                    requires_version=requires_version, requires_modules=requires_modulers)


def update(isamAppliance, service_name, address, active, new_address, new_port, weight, secure=False, ssllabel=None,
           check_mode=False,
           force=False):
    """
    Updating server
    """
    change_required = _check_update(isamAppliance, service_name, address, active, new_address, new_port, weight, secure,
                                    ssllabel)

    if force is True or change_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_put("Updating a server",
                                            "{0}{1}/servers/{2}".format(module_uri, service_name, address),
                                            {
                                                "address": new_address,
                                                "active": active,
                                                "port": new_port,
                                                "weight": weight,
                                                "secure": secure,
                                                "ssllabel": ssllabel

                                            },
                                            requires_modules=requires_modulers,
                                            requires_version=requires_version)
    else:
        return isamAppliance.create_return_object()


def _check_update(isamAppliance, service_name, address, active, new_address, new_port, weight, secure=False,
                  ssllabel=None):
    """
    idempontency test
    """
    org_obj = get(isamAppliance, service_name, address)

    if org_obj['data']['address'] != new_address:
        return True
    elif org_obj['data']['active'] != active:
        return True
    elif org_obj['data']['port'] != new_port:
        return True
    elif org_obj['data']['weight'] != weight:
        return True
    elif org_obj['data']['secure'] != secure:
        return True
    elif org_obj['data']['ssllabel'] != ssllabel:
        return True
    else:
        return False


def _check_exist(isamAppliance, service_name, address):
    """
    idempotency test for delete function
    """
    check_obj = {}
    # Check weather the address with corresponding server exists
    try:
        check_obj = get(isamAppliance, service_name, address)
    except:
        return False

    return True


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
