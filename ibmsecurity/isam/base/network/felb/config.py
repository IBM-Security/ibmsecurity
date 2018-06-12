# TODO needs work


module_uri = "/isam/felb"
requires_module = None  # TODO find this out and for version
requires_version = None


def exp_config(isamAppilance, check_mode=False, force=False):
    """
    Exporting current FELB configuration with RESTful web service
    """
    return isamAppilance.invoke_get("Exporting Configuration", "{0}?export=true".format(module_uri))



def imp_config(isamAppliance, file, check_mode=False, force=False):
    """
    Importing FELB file
    """
    if force is True or check_mode(isamAppliance, file) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Importing Configuration", "{0}".format(module_uri),
                                             {
                                                 "file": file
                                             })  # TODO stopping point till i can talk to someone about it


def replace(isamAppliance, enable=False, debug=False, ha_enable=False, is_primary=False, interface=None,
           remote=None, port=None, health_check_interval=None, health_check_timeout=None, local=False, remote_address=None,
           remote_port=None, remote_facility=None, ssl_enable=False, keyfile=None, services_enable=False, name=None, services_address=None,
           services_port=None, netmask=None, services_interface=None, scheduler=None, services_health_check_interval=None, rise=None, fall=None,
            layer_type=None, layer7_secure=None, layer7_ssl_label=None, layer7_cookie=None, attribute_name=None, attribute_value=None, server_id=None,
           server_active=False, server_address=None, server_port=None, server_weight=None, server_secure=False, ssllabel=None):
    """
    updates ssl configuration
    """
    return isamAppliance.invoke_put("Updating Configuration", "{0}".format(module_uri),
                                    {
                                        "enable": enable,
                                        "debug": debug,
                                        "ha":{
                                            "enable": ha_enable,
                                            "is_primary": is_primary,
                                            "interface": interface,
                                            "remote": remote,
                                            "port": port,
                                            "health_check_interval": health_check_interval,
                                            "health_check_timeout": health_check_timeout
                                            },
                                        "logging":{
                                            "local": local,
                                            "remote_address": remote_address,
                                            "remote_port": remote_port,
                                            "remote_facility": remote_facility
                                            },
                                        "ssl":{
                                            "enable": ssl_enable,
                                            "keyfile": keyfile
                                            },
                                        "services":[
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
                                                "attributes":[
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
                                        "attributes": [
                                            {
                                                "name": attribute_name, # TODO not sure if these two are right
                                                "value": attribute_value
                                            }
                                        ]

                                    })

def get(isamAppliance):
    """
    Retrieves configuration in full
    :param isamAppliance:
    :return:
    """
    return isamAppliance.invoke_get("Retrieving Configuration",module_uri)


def get_config(isamAppliance, check_mode=False, force=False):
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
    return isamAppliance.invoke_put("Updating configuration", "{0}/configuration/{1}".format(module_uri, felb_id),
                                    {
                                        "value": value
                                    })
