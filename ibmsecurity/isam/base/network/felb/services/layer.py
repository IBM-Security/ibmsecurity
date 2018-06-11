import ibmsecurity.utilities.tools

module_uri="/isam/felb/configuration/services/"
requires_modulars=None
requires_version=None


def get(isamAppliance, service_name, check_mode=False, force=False):
    """
    Retrieves layer configuration
    """
    return isamAppliance.invoke_get("Retrieving Layer Configuration", "{0}{1}/layer".format(module_uri, service_name))


def update(isamAppliance, service_name, type, layer7_secure, layer7_ssl_label, layer7_cookie, check_mode=False, force=False):
    """
    Updates specified service name layer
    """
    change_required, json_data = _check(isamAppliance, service_name, type, layer7_secure, layer7_ssl_label, layer7_cookie)

    if force is True or check_mode is False:
        if change_required is True:
            return isamAppliance.invoke_put("Updating Service Layer", "{0}{1}/layer".format(module_uri, service_name), json_data)
        else:
            return isamAppliance.create_return_object(changed=False)

def _check(isamAppliance, service_name,  type, layer7_secure, layer7_ssl_label, layer7_cookie):
    """
    Checks update for idempotency
    """
    change_required=False
    json_data = {
        "type": type,
        "layer7_secure": layer7_secure,
        "layer7_ssl_label": layer7_ssl_label,
        "layer": layer7_cookie
    }
    ret_obj = get(isamAppliance, service_name)

    sort_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
    sort_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj)

    if sort_json_data != sort_ret_obj:
        change_required=True


    return change_required, json_data