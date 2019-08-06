import logging
import ibmsecurity.utilities.tools
import ibmsecurity.isam.base.network.interfaces

logger = logging.getLogger(__name__)

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all static routes
    """
    return isamAppliance.invoke_get("Retrieving all static routes",
                                    "/net/routes")


def get(isamAppliance, uuid, check_mode=False, force=False):
    """
    Retrieving a single static route
    """
    return isamAppliance.invoke_get("Retrieving a single static route",
                                    "/net/routes/{0}".format(uuid))


def add(isamAppliance, address, enabled=True, maskOrPrefix=None, gateway=None, label=None, vlanId=None, metric=None,
        comment='', table='main', check_mode=False, force=False):
    """
    Creating a static route
    """
    warnings = []
    interfaceUUID = _get_interfaceUUID(isamAppliance, label, vlanId)
    if interfaceUUID is None and label is not None:
        warnings.append("Interface {0} not found, Add static route is not supported.".format(label))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)
    if maskOrPrefix is None:
        maskOrPrefix = ""
    if isinstance(maskOrPrefix, basestring):
        if maskOrPrefix.lower() == 'none':
            maskOrPrefix = ""
    if isinstance(table, basestring):
        if table.lower() == 'none':
            table = None
    if isinstance(metric, basestring):
        if metric.lower() == 'none':
            metric = None
        else:
            metric = int(metric)

    if force is True or _check(isamAppliance, address, interfaceUUID) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a static route",
                "/net/routes",
                {
                    "_isNew": True,
                    "enabled": enabled,
                    "address": address,
                    "maskOrPrefix": maskOrPrefix,
                    "gateway": gateway,
                    "interfaceUUID": interfaceUUID,
                    "metric": metric,
                    "comment": comment,
                    "table": table
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, address, new_address=None, enabled=True, maskOrPrefix=None, gateway=None, label=None,
           vlanId=None, new_label=None, new_vlanId=None, metric=None, comment='', table=None, check_mode=False,
           force=False):
    """
    Updating a static route
    """
    warnings = []
    interfaceUUID = _get_interfaceUUID(isamAppliance, label, vlanId)
    if interfaceUUID is None and label is not None:
        warnings.append("Interface {0} not found, Update static route is not supported.".format(label))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)
    uuid = _get_uuid(isamAppliance, address, interfaceUUID)
    if uuid is None:
        logger.info("Unable to find Static Route to modify: {0} / {1}".format(address, interfaceUUID))
        return isamAppliance.create_return_object()
    if new_label is not None:
        interfaceUUID = _get_interfaceUUID(isamAppliance, new_label, new_vlanId)
    if interfaceUUID is None:
        interfaceUUID = ''
    if new_address is not None:
        address = new_address
    if maskOrPrefix is None:
        maskOrPrefix = ''
    if isinstance(maskOrPrefix, basestring):
        if maskOrPrefix.lower() == 'none':
            maskOrPrefix = ''
    if isinstance(table, basestring):
        if table.lower() == 'none':
            table = None
    if isinstance(metric, basestring):
        if metric.lower() == 'none':
            metric = None
        else:
            metric = int(metric)
    if isinstance(enabled, basestring):
        if enabled.lower() == 'true':
            enabled = True
        else:
            enabled = False

    json_data = {
        "enabled": enabled,
        "address": address,
        "maskOrPrefix": maskOrPrefix,
        "gateway": gateway,
        "interfaceUUID": interfaceUUID,
        "metric": metric,
        "comment": comment,
        "table": table,
        "objType": "staticRoute",
        "uuid": uuid
    }

    if force is True or _compare(isamAppliance, json_data) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating a static route",
                "/net/routes/{0}".format(uuid), json_data)

    return isamAppliance.create_return_object()


def _get_interfaceUUID(isamAppliance, label, vlanId):
    if label is None:
        interfaceUUID = None
    else:
        intf = ibmsecurity.isam.base.network.interfaces._get_interface(isamAppliance, label, vlanId)
        interfaceUUID = intf['uuid']

    return interfaceUUID


def _get_uuid(isamAppliance, address, interfaceUUID):
    ret_obj = get_all(isamAppliance)
    for sr in ret_obj['data']['staticRoutes']:
        logger.debug("Scanning {0}/{1} in Static Routes: {2}".format(address, interfaceUUID, sr))
        if sr['address'] == address and (
                sr['interfaceUUID'] == interfaceUUID or (sr['interfaceUUID'] == '' and interfaceUUID is None)):
            return sr['uuid']

    return None


def delete(isamAppliance, address, label, vlanId=None, check_mode=False, force=False):
    """
    Delete a static route
    """
    warnings = []
    interfaceUUID = _get_interfaceUUID(isamAppliance, label, vlanId)
    if interfaceUUID is None and label is not None:
        warnings.append("Interface {0} not found, Delete static route is not supported.".format(label))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)
    uuid = _get_uuid(isamAppliance, address, interfaceUUID)

    if force is True or uuid is not None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a static route",
                "/net/routes/{0}".format(uuid))

    return isamAppliance.create_return_object()


def _check(isamAppliance, address, interfaceUUID):
    """
    Check if static route already exists
    """
    ret_obj = get_all(isamAppliance)

    for sr in ret_obj['data']['staticRoutes']:
        if sr['address'] == address and sr['interfaceUUID'] == interfaceUUID:
            return True

    return False


def _compare(isamAppliance, json_data):
    """
    Check if static route already exists
    """
    ret_obj = get_all(isamAppliance)

    for sr in ret_obj['data']['staticRoutes']:
        if sr['address'] == json_data['address'] and sr['interfaceUUID'] == json_data['interfaceUUID']:
            logger.debug(ibmsecurity.utilities.tools.json_sort(sr))
            logger.debug(ibmsecurity.utilities.tools.json_sort(json_data))
            return ibmsecurity.utilities.tools.json_sort(sr) == ibmsecurity.utilities.tools.json_sort(json_data)

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare static routes between 2 appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for sr in ret_obj1['data']['staticRoutes']:
        del sr['uuid']
        del sr['interfaceUUID']
    for sr in ret_obj2['data']['staticRoutes']:
        del sr['uuid']
        del sr['interfaceUUID']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid', 'interfaceUUID'])
