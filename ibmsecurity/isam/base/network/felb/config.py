import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

module_uri = "/isam/felb"
requires_module = None
requires_version = None


def export(isamAppilance, check_mode=False, force=False):
    """
    Exporting current FELB configuration with RESTful web service
    """
    return isamAppilance.invoke_get("Exporting FELB configuration", "{0}?export=true".format(module_uri),
                                    requires_modules=requires_module, requires_version=requires_version)


def imp_config(isamAppliance, file, check_mode=False, force=False):
    """
    Importing FELB file
    """
    change_required = _check_import(isamAppliance, file)

    if force is True or change_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Importing Configuration", "{0}".format(module_uri),
                                             {
                                                 "file": file
                                             }, requires_version=requires_version,
                                             requires_modules=requires_module)
    else:
        return isamAppliance.create_return_object(changed=False)


def replace(isamAppliance, enable, debug, ha_enable, is_primary, interface,
            remote, port, health_check_interval, health_check_timeout, local, remote_address,
            remote_port, remote_facility, ssl_enable, keyfile, services_enable, name, services_address,
            services_port, netmask, services_interface, scheduler, services_health_check_interval, rise, fall,
            layer_type, layer7_secure, layer7_ssl_label, layer7_cookie, attribute_name, attribute_value, server_id,
            server_active, server_address, server_port, server_weight, server_secure=False, ssllabel=None,
            check_mode=False, force=False):
    """
    updates ssl configuration
    """
    if force is True or _check(isamAppliance, enable, debug, ha_enable, is_primary, interface,
                               remote, port, health_check_interval, health_check_timeout, local, remote_address,
                               remote_port, remote_facility, ssl_enable, keyfile, services_enable, name,
                               services_address,
                               services_port, netmask, services_interface, scheduler, services_health_check_interval,
                               rise, fall,
                               layer_type, layer7_secure, layer7_ssl_label, layer7_cookie, attribute_name,
                               attribute_value, server_id,
                               server_active, server_address, server_port, server_weight, server_secure=False,
                               ssllabel=None) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_put("Updating Configuration", "{0}".format(module_uri),
                                            {
                                                "enabled": enable,
                                                "debug": debug,
                                                "ha": {
                                                    "enabled": ha_enable,
                                                    "is_primary": is_primary,
                                                    "interface": interface,
                                                    "remote": remote,
                                                    "port": port,
                                                    "health_check_interval": health_check_interval,
                                                    "health_check_timeout": health_check_timeout
                                                },
                                                "logging": {
                                                    "local": local,
                                                    "remote_address": remote_address,
                                                    "remote_port": remote_port,
                                                    "remote_facility": remote_facility
                                                },
                                                "ssl": {
                                                    "enabled": ssl_enable,
                                                    "keyfile": keyfile
                                                },
                                                "services": [
                                                    {
                                                        "enabled": services_enable,
                                                        "name": name,
                                                        "address": services_address,
                                                        "port": services_port,
                                                        "netmask": netmask,
                                                        "interface": services_interface,
                                                        "scheduler": scheduler,
                                                        "health_check_interval": services_health_check_interval,
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
                                                                "ssllabel": ssllabel
                                                            }
                                                        ]

                                                    }

                                                ],

                                            })


def get(isamAppliance):
    """
    Retrieves configuration in full
    :param isamAppliance:
    :return:
    """
    return isamAppliance.invoke_get("Retrieving Configuration", module_uri)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieves configuration
    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    return isamAppliance.invoke_get("Retrieving Configuration", "{0}/configuration".format(module_uri))


def update(isamAppliance, felb_id, value, check_mode=False, force=False):
    """
    updates existing configuration
    :param isamAppliance:
    :param felb_id:
    :param check_mode:
    :param force:
    :return:
    """
    change_required = _check_update(isamAppliance, felb_id, value)
    if force is True or change_required is True:
        return isamAppliance.invoke_put("Updating configuration", "{0}/configuration/{1}".format(module_uri, felb_id),
                                        {
                                            "value": value
                                        })
    else:
        return isamAppliance.create_return_object(changed=False)


def _check_import(isamAppliance, file):
    """
    checks to see if file is already imported
    """

    temp_obj = get(isamAppliance)
    change_required = False
    if temp_obj['file'] != file:
        change_required = True

    return change_required


def _check_update(isamappliance, felb_id, value):
    """
    checks update for value passed
    """
    change_required = False
    temp_obj = isamappliance.invoke_get("Retrieving configuration", "{0}/configuration/{1}".format(module_uri, felb_id))

    if temp_obj['value'] != value:
        change_required = True

    return change_required


def _check(isamAppliance, enable, debug, ha_enable, is_primary, interface,
           remote, port, health_check_interval, health_check_timeout, local, remote_address,
           remote_port, remote_facility, ssl_enable, keyfile, services_enable, name, services_address,
           services_port, netmask, services_interface, scheduler, services_health_check_interval, rise, fall,
           layer_type, layer7_secure, layer7_ssl_label, layer7_cookie, attribute_name, attribute_value, server_id,
           server_active, server_address, server_port, server_weight, server_secure=False, ssllabel=None):
    """
    Checks update in full
    """

    check_obj = get(isamAppliance)
    """
    json_data = {
        "enable": enable,
        "debug": debug,
        "ha": {
            "enable": ha_enable,
            "is_primary": is_primary,
            "interface": interface,
            "remote": remote,
            "port": port,
            "health_check_interval": health_check_interval,
            "health_check_timeout": health_check_timeout
        },
        "logging": {
            "local": local,
            "remote_address": remote_address,
            "remote_port": remote_port,
            "remote_facility": remote_facility
        },
        "ssl": {
            "enable": ssl_enable,
            "keyfile": keyfile
        },
        "services": [
            {
                "enable": services_enable,
                "name": name,
                "address": services_address,
                "port": services_port,
                "netmask": netmask,
                "interface": services_interface,
                "scheduler": scheduler,
                "health_check_interval": services_health_check_interval,
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
                        "ssllabel": ssllabel
                    }
                ]
            }
        ],
    }
    sort_check_obj = ibmsecurity.utilities.tools.json_sort(check_obj)
    sort_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
    print sort_check_obj
    print sort_json_data
    """
    if check_obj['data']['debug'] != debug:
        return True
    if check_obj['data']['enabled'] != enable:
        return True
    if check_obj['data']['ha']['enabled'] != ha_enable:
        return True
    if check_obj['data']['ha']['enabled'] != ha_enable:
        return True
    if check_obj['data']['ha']['health_check_interval'] != health_check_interval:
        return True
    if check_obj['data']['ha']['health_check_timeout'] != health_check_timeout:
        return True
    if check_obj['data']['ha']['interface'] != interface:
        return True
    if check_obj['data']['ha']['is_primary'] != is_primary:
        return True
    if check_obj['data']['ha']['port'] != port:
        return True
    if check_obj['data']['ha']['remote'] != remote:
        return True
    if check_obj['data']['logging']['local'] != local:
        return True
    if check_obj['data']['logging']['remote_address'] != remote_address:
        return True
    if check_obj['data']['logging']['remote_facility'] != remote_facility:
        return True
    if check_obj['data']['logging']['remote_port'] != remote_port:
        return True
    if check_obj['data']['services']['address'] != services_address:
        return True
    if check_obj['data']['services']['enabled'] != services_enable:
        return True
    if check_obj['data']['services']['fall'] != fall:
        return True
    if check_obj['data']['services']['health_check_interval'] != services_health_check_interval:
        return True
    if check_obj['data']['services']['interface'] != services_interface:
        return True
    if check_obj['data']['services']['name'] != name:
        return True
    if check_obj['data']['services']['netmask'] != netmask:
        return True
    if check_obj['data']['services']['port'] != services_port:
        return True
    if check_obj['data']['services']['rise'] != rise:
        return True
    if check_obj['data']['services']['scheduler'] != scheduler:
        return True
    if check_obj['data']['servers']['active'] != server_active:
        return True
    if check_obj['data']['servers']['address'] != server_address:
        return True
    if check_obj['data']['servers']['id'] != server_id:
        return True
    if check_obj['data']['servers']['port'] != server_port:
        return True
    if check_obj['data']['servers']['active'] != server_active:
        return True
    if check_obj['data']['servers']['secure'] != server_secure:
        return True
    if check_obj['data']['servers']['ssllabel'] != ssllabel:
        return True
    if check_obj['data']['servers']['weight'] != server_weight:
        return True
    if check_obj['data']['servers']['layer']['type'] != layer_type:
        return True
    if check_obj['data']['servers']['layer']['layer7_cookie'] != layer7_cookie:
        return True
    if check_obj['data']['servers']['layer']['layer7_secure'] != layer7_secure:
        return True
    if check_obj['data']['servers']['layer']['layer7_ssl_label'] != layer7_ssl_label:
        return True
