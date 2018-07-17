import ibmsecurity.utilities.tools
import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/services"
requires_modules = None
requires_version = None


def add(isamAppliance, enabled, name, address, port, netmask, interface, scheduler, health_check_interval,
        rise, fall, layer_type, layer7_secure, layer7_ssl_label, layer7_cookie, attribute_name,
        attribute_value, server_id, server_active, server_address, server_port, server_weight,
        server_secure=False, server_ssllabel=None, check_mode=False, force=False):
    """
    Creating a service
    """
    if force is True or _check_add(isamAppliance, enabled, name, address, port, netmask, interface, scheduler,
                                   health_check_interval,
                                   rise, fall) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
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
                                                 "layer": {
                                                     "type": layer_type,
                                                     "layer7_secure": layer7_secure,
                                                     "layer7_ssl_label": layer7_ssl_label,
                                                     "layer7_cookie": layer7_cookie
                                                 },
                                                 "attributes": [
                                                     {
                                                         "name": attribute_name,
                                                         "value": attribute_value
                                                     }
                                                 ],
                                                 "servers": [
                                                     {
                                                         "id": server_id,
                                                         "active": server_active,
                                                         "address": server_address,
                                                         "port": server_port,
                                                         "weight": server_weight,
                                                         "secure": server_secure,
                                                         "ssllabel": server_ssllabel
                                                     }
                                                 ]

                                             }, requires_version=requires_version, requires_modules=requires_modules)
    else:
        return isamAppliance.create_return_object()


def delete(isamAppliance, service_name, check_mode=False, force=False):
    """
    deletes service
    """
    if force is True or _check_delete(isamAppliance, service_name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting a service", "{0}/{1}".format(module_uri, service_name),
                                               requires_version=requires_version, requires_modules=requires_modules)
    else:
        return isamAppliance.create_return_object()


def get(isamAppliance, service_name, check_mode=False, force=False):
    """
    Receives a single service
    """
    return isamAppliance.invoke_get(
        "Retrieving a service", "{0}/{1}".format(module_uri, service_name), requires_version=requires_version,
        requires_modules=requires_modules)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Receives all services
    """
    return isamAppliance.invoke_get("Retrieving all service names", module_uri, requires_version=requires_version,
                                    requires_modules=requires_modules)


def update(isamAppliance, service_name, enabled, name, address, port, netmask, interface, scheduler,
           health_check_interval, rise, fall, check_mode=False, force=False):
    """
    updates specified service name
    """
    update_required = _check_update(isamAppliance, service_name, enabled, name, address, port, netmask, interface,
                                    scheduler,
                                    health_check_interval, rise, fall)
    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
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
                                            requires_version=requires_version)
    else:
        return isamAppliance.create_return_object()


def _check_update(isamAppliance, service_name, enabled, name, address, port, netmask, interface, scheduler,
                  health_check_interval,
                  rise, fall):
    try:
        ret_obj = get(isamAppliance, service_name)
    except:
        logger.warning("The requested service does not exist in the configuration.")
        return False

    if ret_obj['data']['enabled'] != enabled:
        return True
    if ret_obj['data']['address'] != address:
        return True
    if ret_obj['data']['fall'] != fall:
        return True
    if ret_obj['data']['health_check_interval'] != health_check_interval:
        return True
    if ret_obj['data']['interface'] != interface:
        return True
    if ret_obj['data']['name'] != name:
        return True
    if ret_obj['data']['netmask'] != netmask:
        return True
    if ret_obj['data']['port'] != port:
        return True
    if ret_obj['data']['rise'] != rise:
        return True
    if ret_obj['data']['scheduler'] != scheduler:
        return True
    else:
        return False


def _check_add(isamAppliance, enabled, name, address, port, netmask, interface, scheduler, health_check_interval,
               rise, fall):
    ret_obj = {}
    # checks to see if service exists
    try:
        ret_obj = get(isamAppliance, name)
    except:
        return True

    if ret_obj['data']['name'] == name:
        logger.warning("Server Already Exist")
        return False

    if ret_obj['data']['enabled'] != enabled:
        return True
    if ret_obj['data']['name'] != name:
        return True
    if ret_obj['data']['address'] != address:
        return True
    if ret_obj['data']['port'] != port:
        return True
    if ret_obj['data']['netmask'] != netmask:
        return True
    if ret_obj['data']['interface'] != interface:
        return True
    if ret_obj['data']['scheduler'] != scheduler:
        return True
    if ret_obj['data']['health_check_interval'] != health_check_interval:
        return True
    if ret_obj['data']['fall'] != fall:
        return True
    if ret_obj['data']['rise'] != rise:
        return True


    else:
        return False


def _check_delete(isamAppliance, service_name):
    """
    idempotency test for delete function
    """
    ret_obj = {}

    try:
        ret_obj = get(isamAppliance, service_name)
    except:
        return False

    if ret_obj['data']['enabled'] == True:
        return True


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
