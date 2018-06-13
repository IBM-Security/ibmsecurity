import ibmsecurity.utilities.tools

module_uri = "/isam/felb/configuration/services"
requires_modules = None
requires_version = None


def add(isamAppliance, enabled, name, address, port, netmask, interface, scheduler, health_check_interval,
           rise, fall, layer_type, layer7_secure, layer7_ssl_label, layer7_cookie, attribute_name,
           attribute_value, server_id, server_active, server_address, server_port, server_weight,
           server_secure=False, server_ssllabel=None, check_mode=False, force=False):
    return isamAppliance.invoke_post("Creating Server", module_uri,
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


def delete(isamAppliance, service_name, check_mode=False, force=False):
    """
    deletes service
    """
    return isamAppliance.invoke_delete("Deleting Service", "{0}/{1}".format(module_uri, service_name))


def get(isamAppliance, service_name, check_mode=False, force=False):
    """
    Receives a single service
    """
    return isamAppliance.invoke_get(
        "Receiving Service:", "{0}/{1}".format(module_uri, service_name))


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Receives all services
    """
    return isamAppliance.invoke_get("Receiving all Services", module_uri)


def update(isamAppliance, service_name, enabled, name, address, port, netmask, interface, scheduler,
           health_check_interval, rise, fall, check_mode=False, force=False):
    """
    updates specified service name
    """
    update_required, json_data = _check(isamAppliance, service_name=service_name, enabled=enabled, name=name,
                                        address=address,
                                        port=port, netmask=netmask, interface=interface, scheduler=scheduler,
                                        health_check_interval=health_check_interval, rise=rise, fall=fall)
    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating High Availability", "{0}/{1}".format(module_uri, service_name),
                                            json_data, requires_modules=requires_modules,
                                            requires_version=requires_version)
    if update_required is False:
        return isamAppliance.create_return_object(changed=False)


def _check(isamAppliance, service_name, enabled, name, address, port, netmask, interface, scheduler,
           health_check_interval,
           rise, fall, check_mode=False, force=False):
    ret_obj = get(isamAppliance, service_name)
    change_required = False
    json_data = {

        "enable": enabled,
        "name": name,
        "address": address,
        "port": port,
        "netmask": netmask,
        "interface": interface,
        "scheduler": scheduler,
        "health_check_interval": health_check_interval,
        "rise": rise,
        "fall": fall
    }

    sort_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj)
    sort_json_data = ibmsecurity.utilities.tools.json_sort(json_data)

    if sort_json_data != sort_ret_obj:
        change_required = True

    return change_required, json_data


def _check_create(isamAppliance, enabled, name, address, port, netmask, interface, scheduler, health_check_interval,
                  rise, fall, layer_type, layer7_secure, layer7_ssl_label, layer7_cookie, attribute_name,
                  attribute_value, server_id, server_active, server_address, server_port, server_weight,
                  server_secure=False, server_ssllabel=None):
    ret_obj = get(isamAppliance, name)
    change_required = False

    json_data = {
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
    }

    sort_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
    sort_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj)

    if sort_ret_obj != sort_json_data:
        change_required = True

    return change_required, json_data
