import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get all snmp objects
    """
    return isamAppliance.invoke_get("Get all snmp objects",
                                    "/core/rsp_snmp_objs")


def get(isamAppliance, uuid, check_mode=False, force=False):
    """
    Get a specific snmp object
    """
    return isamAppliance.invoke_get("Get a specific snmp object",
                                    f"/core/rsp_snmp_objs/{uuid}")


def add(isamAppliance, name, trapAddress, trapCommunity, trapNotificationType=None, trapVersion='V1', trapPort=162,
        objType='snmp', username=None, authEnabled=None, authType=None, authPassPhrase=None, privEnabled=None,
        privType=None, privPassPhrase=None, informSnmpEngineID=None, informTimeout=None, comment='', check_mode=False,
        force=False):
    """
    Add a snmp object
    """
    if force is True or _check(isamAppliance, None, name, trapAddress, trapCommunity, trapNotificationType, trapVersion,
                               trapPort, objType, username, authEnabled, authType, authPassPhrase, privEnabled,
                               privType, privPassPhrase, informSnmpEngineID, informTimeout, comment) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add a snmp object",
                "/core/rsp_snmp_objs/",
                {
                    'name': name,
                    'objType': objType,
                    'comment': comment,
                    'trapAddress': trapAddress,
                    'trapPort': trapPort,
                    'trapCommunity': trapCommunity,
                    'trapVersion': trapVersion,
                    'trapNotificationType': trapNotificationType,
                    'userName': username,
                    'authEnabled': authEnabled,
                    'authType': authType,
                    'authPassPhrase': authPassPhrase,
                    'privEnabled': privEnabled,
                    'privType': privType,
                    'privPassPhrase': privPassPhrase,
                    'informSnmpEngineID': informSnmpEngineID,
                    'informTimeout': informTimeout
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, uuid, name, trapAddress, trapCommunity, trapNotificationType=None, trapVersion='V1',
           trapPort=162, objType='snmp', username=None, authEnabled=None, authType=None, authPassPhrase=None,
           privEnabled=None, privType=None, privPassPhrase=None, informSnmpEngineID=None, informTimeout=None,
           comment='', check_mode=False, force=False):
    """
    Update a specific snmp object
    """
    if force is True or (
            _exists(isamAppliance, uuid) is True and _check(isamAppliance, uuid, name, trapAddress,
                                                            trapCommunity, trapNotificationType, trapVersion,
                                                            trapPort, objType, username, authEnabled, authType,
                                                            authPassPhrase, privEnabled, privType,
                                                            privPassPhrase, informSnmpEngineID, informTimeout,
                                                            comment) is False):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specific snmp object",
                f"/core/rsp_snmp_objs/{uuid}",
                {
                    'name': name,
                    'uuid': uuid,
                    'objType': objType,
                    'comment': comment,
                    'trapAddress': trapAddress,
                    'trapPort': trapPort,
                    'trapCommunity': trapCommunity,
                    'trapVersion': trapVersion,
                    'trapNotificationType': trapNotificationType,
                    'userName': username,
                    'authEnabled': authEnabled,
                    'authType': authType,
                    'authPassPhrase': authPassPhrase,
                    'privEnabled': privEnabled,
                    'privType': privType,
                    'privPassPhrase': privPassPhrase,
                    'informSnmpEngineID': informSnmpEngineID,
                    'informTimeout': informTimeout
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, uuid, check_mode=False, force=False):
    """
    Delete a snmp object
    """
    if force is True or _exists(isamAppliance, uuid) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a snmp object",
                f"/core/rsp_snmp_objs/{uuid}")

    return isamAppliance.create_return_object()


def _exists(isamAppliance, uuid):
    """
    Check if an uuid object exists

    :param isamAppliance:
    :param uuid:
    :return:
    """
    exists = False
    ret_obj = get_all(isamAppliance)

    for snmp in ret_obj['data']['snmpObjects']:
        if snmp['uuid'] == uuid:
            exists = True
            break

    return exists


def _check(isamAppliance, uuid, name, trapAddress, trapCommunity, trapNotificationType, trapVersion, trapPort, objType,
           username, authEnabled, authType, authPassPhrase, privEnabled, privType, privPassPhrase, informSnmpEngineID,
           informTimeout, comment):
    """
    Check if the snmp object exists and is the same - uuid=None means add versus delete

    NOTE: if UUID is not found that will be same as no match!!!
    """

    set_value = {
        'name': name,
        'uuid': uuid,
        'objType': objType,
        'comment': comment,
        'trapAddress': trapAddress,
        'trapPort': trapPort,
        'trapCommunity': trapCommunity,
        'trapVersion': trapVersion,
        'trapNotificationType': trapNotificationType,
        'userName': username,
        'authEnabled': authEnabled,
        'authType': authType,
        'authPassPhrase': authPassPhrase,
        'privEnabled': privEnabled,
        'privType': privType,
        'privPassPhrase': privPassPhrase,
        'informSnmpEngineID': informSnmpEngineID,
        'informTimeout': informTimeout
    }

    set_value = ibmsecurity.utilities.tools.json_sort(set_value)

    ret_obj = get_all(isamAppliance)
    for obj in ret_obj['data']['snmpObjects']:
        if uuid is None and obj['name'] == name:
            return True
        elif ibmsecurity.utilities.tools.json_sort(obj) == set_value:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare snmp objects between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']['snmpObjects']:
        del obj['uuid']
    for obj in ret_obj2['data']['snmpObjects']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
