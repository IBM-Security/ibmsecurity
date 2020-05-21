import logging
import ibmsecurity.utilities.tools
import ibmsecurity.isam.base.network.interfaces

logger = logging.getLogger(__name__)
requires_model="Appliance"

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all static routes
    """
    return isamAppliance.invoke_get("Retrieving all static routes",
                                    "/net/routes", requires_model=requires_model)


def get(isamAppliance, uuid, check_mode=False, force=False):
    """
    Retrieving a single static route
    """
    return isamAppliance.invoke_get("Retrieving a single static route",
                                    "/net/routes/{0}".format(uuid), requires_model=requires_model)


def add(isamAppliance, address, enabled=True, comment='', table='main', maskOrPrefix=None, gateway=None, label=None,
        vlanId=None, metric=None, check_mode=False, force=False):
    """
    Creating a static route
    """

    if isamAppliance.facts['model'] != requires_model:
        warnings = ["API invoked requires model: {0}, appliance is of deployment model: {1}.".format(requires_model, isamAppliance.facts['model'])]
        return isamAppliance.create_return_object(warnings=warnings)

    if table.lower() != 'main':
        table_uuid = ibmsecurity.isam.base.network.interfaces.search(isamAppliance, address=table)
        if table_uuid['data'] != {}:
            table = table_uuid['data']
        else:
            ret_obj = ibmsecurity.isam.base.network.interfaces.get_all(isamAppliance)
            found_table = False
            interfaces = ret_obj['data']['interfaces']
            for obj in interfaces:
                items = obj['ipv4']['addresses']
                for item in items:
                    if item['uuid'] == table:
                        found_table = True
            if found_table is False:
                logger.debug("Route table {0} is not found, Add static route is not supported.".format(table))
                return isamAppliance.create_return_object(changed=False)

    interfaceUUID = _get_interfaceUUID(isamAppliance, label, vlanId)
    if interfaceUUID is None and label is not None:
        logger.debug("Interface {0} not found, Add static route is not supported.".format(label))
        return isamAppliance.create_return_object(changed=False)

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

    if force is True or _check(isamAppliance=isamAppliance, address=address, table=table,
                               interfaceUUID=interfaceUUID) is False:
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


def update(isamAppliance, address, new_address=None, enabled=True, maskOrPrefix=None, gateway=None,
           metric=None, comment='', table='main', label=None, vlanId=None, new_label=None, new_vlanId=None,
           check_mode=False, force=False):
    """
    Updating a static route
    """
    if isamAppliance.facts['model'] != requires_model:
        warnings = ["API invoked requires model: {0}, appliance is of deployment model: {1}.".format(requires_model, isamAppliance.facts['model'])]
        return isamAppliance.create_return_object(warnings=warnings)

    warnings = []
    interfaceUUID = _get_interfaceUUID(isamAppliance, label, vlanId)
    if interfaceUUID is None and label is not None:
        warnings.append("Interface {0} not found, Update static route is not supported.".format(label))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)

    if table.lower() != 'main':
        table_uuid = ibmsecurity.isam.base.network.interfaces.search(isamAppliance, address=table)
        if table_uuid['data'] != {}:
            table = table_uuid['data']
        else:
            ret_obj = ibmsecurity.isam.base.network.interfaces.get_all(isamAppliance)
            found_table = False
            interfaces = ret_obj['data']['interfaces']
            for obj in interfaces:
                items = obj['ipv4']['addresses']
                for item in items:
                    if item['uuid'] == table:
                        found_table = True
            if found_table is False:
                logger.debug("Route table {0} is not found, Add static route is not supported.".format(table))
                return isamAppliance.create_return_object(changed=False)

    uuid = _get_uuid(isamAppliance, address, table, interfaceUUID)

    if uuid is None:
        logger.info("Unable to find Static Route to modify: {0} / {1}".format(address, table))
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


def set(isamAppliance, address, new_address=None, enabled=True, maskOrPrefix=None, gateway=None, metric=None,
        comment='', table='main', label=None, vlanId=None, new_label=None, new_vlanId=None, check_mode=False,
        force=False):

    if isamAppliance.facts['model'] != requires_model:
        warnings = ["API invoked requires model: {0}, appliance is of deployment model: {1}.".format(requires_model, isamAppliance.facts['model'])]
        return isamAppliance.create_return_object(warnings=warnings)

    if table != 'main':
        table_uuid = ibmsecurity.isam.base.network.interfaces.search(isamAppliance, address=table)
        table_uuid = table_uuid['data']
    else:
        table_uuid = 'main'

    warnings = []
    interfaceUUID = _get_interfaceUUID(isamAppliance, label, vlanId)
    if interfaceUUID is None and label is not None:
        warnings.append("Interface {0} not found, Update static route is not supported.".format(label))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)

    if _check(isamAppliance, address, table_uuid, interfaceUUID) is True:
        return update(isamAppliance=isamAppliance, address=address, new_address=new_address, enabled=enabled,
                      maskOrPrefix=maskOrPrefix, gateway=gateway, label=label,
                      vlanId=vlanId, new_label=new_label, new_vlanId=new_vlanId, metric=metric, comment=comment,
                      table=table, check_mode=check_mode, force=force)
    else:
        return add(isamAppliance=isamAppliance, address=address, enabled=enabled, maskOrPrefix=maskOrPrefix,
                   gateway=gateway, label=label, vlanId=vlanId,
                   metric=metric, comment=comment, table=table, check_mode=check_mode, force=force)


def _get_interfaceUUID(isamAppliance, label, vlanId=None):
    if label is None or label == '' or label.lower() == 'auto':
        interfaceUUID = ''
    else:
        intf = ibmsecurity.isam.base.network.interfaces._get_interface(isamAppliance, label, vlanId)
        interfaceUUID = intf['uuid']

    return interfaceUUID


def _get_uuid(isamAppliance, address, table, interfaceUUID):
    ret_obj = get_all(isamAppliance)
    for sr in ret_obj['data']['staticRoutes']:
        logger.debug("Scanning {0}/{1}/{2} in Static Routes: {3}".format(address, table, interfaceUUID, sr))
        if sr['address'] == address and (
                sr['interfaceUUID'] == interfaceUUID or (sr['interfaceUUID'] == '' and interfaceUUID is None)) and sr[
            'table'] == table:
            return sr['uuid']

    return None


def delete(isamAppliance, address, table='main', label=None, vlanId=None, check_mode=False, force=False):
    """
    Delete a static route
    """
    if isamAppliance.facts['model'] != requires_model:
        warnings = ["API invoked requires model: {0}, appliance is of deployment model: {1}.".format(requires_model, isamAppliance.facts['model'])]
        return isamAppliance.create_return_object(warnings=warnings)

    warnings = []
    interfaceUUID = _get_interfaceUUID(isamAppliance, label, vlanId)

    if interfaceUUID is None and label is not None:
        warnings.append("Interface {0} not found, Delete static route is not supported.".format(label))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)

    if table != 'main':
        table_uuid = ibmsecurity.isam.base.network.interfaces.search(isamAppliance, address=table)
        if table_uuid['data'] != {}:
            table = table_uuid['data']
        else:
            ret_obj = ibmsecurity.isam.base.network.interfaces.get_all(isamAppliance)
            found_table = False
            interfaces = ret_obj['data']['interfaces']
            for obj in interfaces:
                items = obj['ipv4']['addresses']
                for item in items:
                    if item['uuid'] == table:
                        found_table = True
            if found_table is False:
                logger.debug("Route table {0} is not found, Add static route is not supported.".format(label))
                return isamAppliance.create_return_object(changed=False)

    uuid = _get_uuid(isamAppliance=isamAppliance, address=address, table=table, interfaceUUID=interfaceUUID)

    if force is True or uuid is not None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a static route",
                "/net/routes/{0}".format(uuid))

    return isamAppliance.create_return_object()


def _check(isamAppliance, address, table, interfaceUUID):
    """
    Check if static route already exists
    """
    ret_obj = get_all(isamAppliance)

    for sr in ret_obj['data']['staticRoutes']:
        if sr['address'] == address and sr['table'] == table and sr['interfaceUUID'] == interfaceUUID:
            return True

    return False


def _compare(isamAppliance, json_data):
    """
    Check if static route already exists
    """
    ret_obj = get_all(isamAppliance)

    for sr in ret_obj['data']['staticRoutes']:
        if sr['address'] == json_data['address'] and sr['table'] == json_data['table'] and sr['interfaceUUID'] == \
                json_data['interfaceUUID']:
            logger.debug(ibmsecurity.utilities.tools.json_sort(sr))
            logger.debug(ibmsecurity.utilities.tools.json_sort(json_data))
            return ibmsecurity.utilities.tools.json_sort(sr) == ibmsecurity.utilities.tools.json_sort(json_data)

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare static routes between 2 appliances
    """
    if isamAppliance1.facts['model'] != requires_model:
        warnings = ["API invoked requires model: {0}, appliance is of deployment model: {1}.".format(requires_model, isamAppliance1.facts['model'])]
        return isamAppliance1.create_return_object(warnings=warnings)

    if isamAppliance2.facts['model'] != requires_model:
        warnings = ["API invoked requires model: {0}, appliance is of deployment model: {1}.".format(requires_model, isamAppliance2.facts['model'])]
        return isamAppliance2.create_return_object(warnings=warnings)

    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for sr in ret_obj1['data']['staticRoutes']:
        del sr['uuid']
        del sr['interfaceUUID']
    for sr in ret_obj2['data']['staticRoutes']:
        del sr['uuid']
        del sr['interfaceUUID']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid', 'interfaceUUID'])
