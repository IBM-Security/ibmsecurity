import ibmsecurity.utilities.tools
import logging

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/services"
requires_modules = None
requires_version = None
requires_model = "Appliance"


def add(isamAppliance, service_name, address, active, port, weight, secure, ssllabel, check_mode=False, force=False):
    """
    Creating a server
    """
    check_exist, warnings = _check_exist(isamAppliance, service_name, address, port)

    if force is True or check_exist is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:

            return isamAppliance.invoke_post("Creating a server",
                                             f"{module_uri}/{service_name}/servers",
                                             {
                                                 "active": active,
                                                 "address": address,
                                                 "port": port,
                                                 "weight": weight,
                                                 "secure": secure,
                                                 "ssllabel": ssllabel

                                             },
                                             requires_version=requires_version, requires_modules=requires_modules, requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, service_name, address, port, check_mode=False, force=False):
    """
    deletes a server from specified service name
    """

    check_exist, warnings = _check_exist(isamAppliance, service_name, address, port)
    if force is True or check_exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            id = address + ":" + str(port)
            return isamAppliance.invoke_delete("Deleting a server",
                                               f"{module_uri}/{service_name}/servers/{id}",
                                               requires_version=requires_version, requires_modules=requires_modules, requires_model=requires_model)

    else:
        return isamAppliance.create_return_object(warnings=warnings)


def get(isamAppliance, service_name, address, port, check_mode=False, force=False):
    """
    Retrieves server from specified service name
    """

    id = address + ":" + str(port)
    return (isamAppliance.invoke_get("Retrieving a server", f"{module_uri}/{service_name}/servers/{id}",
                                 requires_version=requires_version, requires_modules=requires_modules, requires_model=requires_model))


def get_all(isamAppliance, service_name, check_mode=False, force=False):
    """
    Retrieves a list of servers under a specified service
    """
    return isamAppliance.invoke_get("Retrieving servers for a service",
                                    f"{module_uri}/{service_name}/servers",
                                    requires_version=requires_version, requires_modules=requires_modules, requires_model=requires_model)


def update(isamAppliance, service_name, address, active, port, weight, secure=False, ssllabel=None, new_address=None, new_port=None, check_mode=False, force=False):
    """
    Updating server
    """
    id = address + ":" + str(port)
    json_data = {'active': active, 'secure': secure, 'ssllabel': ssllabel, 'weight': weight}
    if new_address is not None:
        json_data['address'] = new_address
    else:
        json_data['address'] = address

    if new_port is not None:
        json_data['port'] = new_port
    else:
        json_data['port'] = port
    change_required, warnings = _check_update(isamAppliance, service_name, address, port, json_data)

    if force is True or change_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:

            return isamAppliance.invoke_put("Updating a server",
                                            f"{module_uri}/{service_name}/servers/{id}",
                                            json_data,
                                            requires_modules=requires_modules,
                                            requires_version=requires_version,
                                            requires_model = requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def _check_update(isamAppliance, service_name, address, port, json_data):
    """
    idempontency test
    """

    ret_obj = get(isamAppliance, service_name, address, port)
    warnings = ret_obj['warnings']

    ret_data = ret_obj['data']

    if 'id' in ret_data:
        del ret_data['id']
    else:
        return False, warnings

    sorted_ret_data = tools.json_sort(ret_data)
    sorted_json_data = tools.json_sort(json_data)
    logger.debug(f"Sorted Existing Data:{sorted_ret_data}")
    logger.debug(f"Sorted Desired  Data:{sorted_json_data}")

    if sorted_ret_data != sorted_json_data:
        return True, warnings
    else:
        return False, warnings


def _check_exist(isamAppliance, service_name, address, port):
    """
    idempotency test for delete function
    """

    id = address + ":" + str(port)
    ret_obj = get_all(isamAppliance, service_name)
    warnings = ret_obj['warnings']

    for obj in ret_obj['data']:
        if obj['id'] == id:
            return True, warnings

    return False, warnings


def compare(isamAppliance1, service_name1, isamAppliance2, service_name2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get_all(isamAppliance1, service_name1)
    ret_obj2 = get_all(isamAppliance2, service_name2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
