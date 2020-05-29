import ibmsecurity.utilities.tools
import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/services"
requires_modules = None
requires_version = None
requires_model = "Appliance"


def add(isamAppliance, enabled, name, address, port, netmask, interface, scheduler, health_check_interval,
        rise, fall, layer, attributes=[], servers=None, check_mode=False, force=False):
    """
    Creating a service
    """

    check_value, warnings = _check_add(isamAppliance, enabled, name, address, port, netmask, interface, scheduler,
                                   health_check_interval, rise, fall)
    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post("Creating a service", module_uri,
                                             {
                                                 "enabled": enabled,
                                                 "name": name,
                                                 "address": address,
                                                 "port": port,
                                                 "netmask": netmask,
                                                 "interface": interface,
                                                 "scheduler": scheduler,
                                                 "health_check_interval": health_check_interval,
                                                 "rise": rise,
                                                 "fall": fall,
                                                 "layer": layer,
                                                 "attributes": attributes,
                                                 "servers": servers

                                             }, requires_version=requires_version, requires_modules=requires_modules, requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, service_name, check_mode=False, force=False):
    """
    deletes service
    """

    check_value, warnings = _check_delete(isamAppliance, service_name)
    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete("Deleting a service", "{0}/{1}".format(module_uri, service_name),
                                               requires_version=requires_version, requires_modules=requires_modules, requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def get(isamAppliance, service_name, check_mode=False, force=False):
    """
    Receives a single service
    """
    return isamAppliance.invoke_get(
        "Retrieving a service", "{0}/{1}".format(module_uri, service_name), requires_version=requires_version,
        requires_modules=requires_modules, requires_model=requires_model)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Receives all services
    """
    return isamAppliance.invoke_get("Retrieving all service names", module_uri, requires_version=requires_version,
                                    requires_modules=requires_modules, requires_model=requires_model)


def update(isamAppliance, service_name, enabled, name, address, port, netmask, interface, scheduler,
           health_check_interval, rise, fall, check_mode=False, force=False):
    """
    updates specified service name
    """

    update_required, warnings = _check_update(isamAppliance, service_name, enabled, name, address, port, netmask, interface,
                                                scheduler, health_check_interval, rise, fall)
    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Updating a service", "{0}/{1}".format(module_uri, service_name),
                                            {
                                                "address": address,
                                                "enabled": enabled,
                                                "fall": fall,
                                                "health_check_interval": health_check_interval,
                                                "interface": interface,
                                                "name": name,
                                                "netmask": netmask,
                                                "port": port,
                                                "rise": rise,
                                                "scheduler": scheduler

                                            }, requires_modules=requires_modules,
                                            requires_version=requires_version,
                                            requires_model = requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def _check_update(isamAppliance, service_name, enabled, name, address, port, netmask, interface, scheduler,
                  health_check_interval, rise, fall):

    warnings = ""
    try:
        ret_obj = get(isamAppliance, service_name)
        warnings =ret_obj['warnings']
    except:
        logger.warning("The requested service does not exist in the configuration.")
        check_value = False
        return check_value, warnings

    if 'enabled' in ret_obj['data']:
        if ret_obj['data']['enabled'] != enabled:
            return True, warnings
        if ret_obj['data']['address'] != address:
            return True, warnings
        if ret_obj['data']['fall'] != fall:
            return True, warnings
        if ret_obj['data']['health_check_interval'] != health_check_interval:
            return True, warnings
        if ret_obj['data']['interface'] != interface:
            return True, warnings
        if ret_obj['data']['name'] != name:
            return True, warnings
        if ret_obj['data']['netmask'] != netmask:
            return True, warnings
        if ret_obj['data']['port'] != port:
            return True, warnings
        if ret_obj['data']['rise'] != rise:
            return True, warnings
        if ret_obj['data']['scheduler'] != scheduler:
            return True, warnings


    return False, warnings


def _check_add(isamAppliance, enabled, name, address, port, netmask, interface, scheduler, health_check_interval,
               rise, fall):
    ret_obj = {}
    # checks to see if service exists
    warnings = ""
    try:
        ret_obj = get(isamAppliance, name)
        warnings = ret_obj['warnings']
    except:
        return True, warnings

    if 'name' in ret_obj['data']:
        if ret_obj['data']['name'] == name:
            logger.warning("Server Already Exist")
            return False, warnings
    else:
        return False, warnings

    if ret_obj['data'] != {}:
        if ret_obj['data']['enabled'] != enabled:
            return True, warnings
        if ret_obj['data']['name'] != name:
            return True, warnings
        if ret_obj['data']['address'] != address:
            return True, warnings
        if ret_obj['data']['port'] != port:
            return True, warnings
        if ret_obj['data']['netmask'] != netmask:
            return True, warnings
        if ret_obj['data']['interface'] != interface:
            return True, warnings
        if ret_obj['data']['scheduler'] != scheduler:
            return True, warnings
        if ret_obj['data']['health_check_interval'] != health_check_interval:
            return True, warnings
        if ret_obj['data']['fall'] != fall:
            return True, warnings
        if ret_obj['data']['rise'] != rise:
            return True, warnings


    return False, warnings


def _check_delete(isamAppliance, service_name):
    """
    idempotency test for delete function
    """
    ret_obj = {}
    warnings = ""

    try:
        ret_obj = get(isamAppliance, service_name)
        warnings = ret_obj['warnings']
    except:
        return False, warnings

    if 'enabled' in ret_obj['data']:
        if ret_obj['data']['enabled'] == True:
            return True, warnings

    return False, warnings


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
