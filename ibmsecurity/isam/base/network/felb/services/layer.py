import ibmsecurity.utilities.tools
import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/services/"
requires_modulers = None
requires_version = None


def get(isamAppliance, service_name, check_mode=False, force=False):
    """
    Retrieves layer configuration
    """
    return isamAppliance.invoke_get("Retrieving Layer Configuration", "{0}{1}/layer".format(module_uri, service_name),
                                    requires_version=requires_version, requires_modules=requires_modulers)


def update(isamAppliance, service_name, type, layer7_secure, layer7_ssl_label, layer7_cookie=None, check_mode=False,
           force=False):
    """
    Updates specified service name layer
    """
    change_required = _check(isamAppliance, service_name, type, layer7_secure, layer7_ssl_label, layer7_cookie)

    if force is True or change_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating Service Layer", "{0}{1}/layer".format(module_uri, service_name),
                                            {
                                                "type": type,
                                                "layer7_secure": layer7_secure,
                                                "layer7_ssl_label": layer7_ssl_label,
                                                "layer7_cookie": layer7_cookie

                                            }, requires_version=requires_version, requires_modules=requires_modulers)
    else:
        return isamAppliance.create_return_object()


def _check(isamAppliance, service_name, type, layer7_secure, layer7_ssl_label, layer7_cookie):
    """
    Checks update for idempotency
    """

    ret_obj = get(isamAppliance, service_name)
    if ret_obj['data']['type'] != type:
        return True
    elif ret_obj['data']['layer7_secure'] != layer7_secure:
        return True
    elif ret_obj['data']['layer7_ssl_label'] != layer7_ssl_label:
        return True
    elif ret_obj['data']['layer7_cookie'] != layer7_cookie:
        return True
    else:
        return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
