import ibmsecurity.utilities.tools

module_uri="/isam/felb/configuration/services/"
requires_modulers=None
requires_version=None


def get(isamAppliance, service_name, check_mode=False, force=False):
    """
    Retrieves layer configuration
    """
    return isamAppliance.invoke_get("Retrieving Layer Configuration", "{0}{1}/layer".format(module_uri, service_name))


def update(isamAppliance, service_name, type, layer7_secure, layer7_ssl_label, layer7_cookie=None, check_mode=False, force=False):
    """
    Updates specified service name layer
    """
    change_required = _check(isamAppliance, service_name, type, layer7_secure, layer7_ssl_label, layer7_cookie)

    if force is True or change_required is True:
        return isamAppliance.invoke_put("Updating Service Layer", "{0}{1}/layer".format(module_uri, service_name),
                                        {
                                            "type": type,
                                            "layer7_secure": layer7_secure,
                                            "layer7_ssl_label": layer7_ssl_label,
                                            "layer7_cookie": layer7_cookie

                                        }, requires_version=requires_version, requires_modules=requires_modulers)
    else:
        return isamAppliance.create_return_object(changed=False)

def _check(isamAppliance, service_name,  type, layer7_secure, layer7_ssl_label, layer7_cookie):
    """
    Checks update for idempotency
    """
    change_required=False
    ret_obj = get(isamAppliance, service_name)
    if ret_obj['data']['type'] != type:
        change_required=True
    elif ret_obj['data']['layer7_secure'] != layer7_secure:
        change_required=True
    elif ret_obj['data']['layer7_ssl_label'] != layer7_ssl_label:
        change_required=True
    elif ret_obj['data']['layer7_cookie'] != layer7_cookie:
        change_required=True


    return change_required