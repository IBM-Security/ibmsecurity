import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isdsAppliance, check_mode=False, force=False):
    """
    Get all snmp objects
    """
    return isdsAppliance.invoke_get("Get all snmp objects",
                                    "/rsp_snmp_objs")


def get(isdsAppliance, uuid, check_mode=False, force=False):
    """
    Get a specific snmp object
    """
    return isdsAppliance.invoke_get("Get a specific snmp object",
                                    "/rsp_snmp_objs/{0}".format(uuid))


def add(isdsAppliance, name, trapAddress, trapCommunity, trapNotificationType=None, trapVersion='V1', trapPort=162,
        objType='snmp', username=None, authEnabled=None, authType=None, authPassPhrase=None, privEnabled=None,
        privType=None, privPassPhrase=None, informSnmpEngineID=None, informTimeout=None, comment='', check_mode=False,
        force=False):
    """
    Add a snmp object
    """
    if force is True or _check(isdsAppliance, None, name, trapAddress, trapCommunity, trapNotificationType, trapVersion,
                               trapPort, objType, username, authEnabled, authType, authPassPhrase, privEnabled,
                               privType, privPassPhrase, informSnmpEngineID, informTimeout, comment) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post(
                "Add a snmp object",
                "/rsp_snmp_objs/",
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

    return isdsAppliance.create_return_object()


def update(isdsAppliance, uuid, name, trapAddress, trapCommunity, trapNotificationType=None, trapVersion='V1',
           trapPort=162, objType='snmp', username=None, authEnabled=None, authType=None, authPassPhrase=None,
           privEnabled=None, privType=None, privPassPhrase=None, informSnmpEngineID=None, informTimeout=None,
           comment='', check_mode=False, force=False):
    """
    Update a specific snmp object
    """
    if force is True or (
            _exists(isdsAppliance, uuid) is True and _check(isdsAppliance, uuid, name, trapAddress,
                                                            trapCommunity, trapNotificationType, trapVersion,
                                                            trapPort, objType, username, authEnabled, authType,
                                                            authPassPhrase, privEnabled, privType,
                                                            privPassPhrase, informSnmpEngineID, informTimeout,
                                                            comment) is False):
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_put(
                "Update a specific snmp object",
                "/rsp_snmp_objs/{0}".format(uuid),
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

    return isdsAppliance.create_return_object()


def delete(isdsAppliance, uuid, check_mode=False, force=False):
    """
    Delete a snmp object
    """
    if force is True or _exists(isdsAppliance, uuid) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_delete(
                "Delete a snmp object",
                "/rsp_snmp_objs/{0}".format(uuid))

    return isdsAppliance.create_return_object()


def _exists(isdsAppliance, uuid):
    """
    Check if an uuid object exists

    :param isdsAppliance:
    :param uuid:
    :return:
    """
    exists = False
    ret_obj = get_all(isdsAppliance)

    for snmp in ret_obj['data']['snmpObjects']:
        if snmp['uuid'] == uuid:
            exists = True
            break

    return exists


def _check(isdsAppliance, uuid, name, trapAddress, trapCommunity, trapNotificationType, trapVersion, trapPort, objType,
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

    ret_obj = get_all(isdsAppliance)
    for obj in ret_obj['data']['snmpObjects']:
        if uuid is None and obj['name'] == name:
            return True
        elif ibmsecurity.utilities.tools.json_sort(obj) == set_value:
            return True

    return False


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare snmp objects between two appliances
    """
    ret_obj1 = get_all(isdsAppliance1)
    ret_obj2 = get_all(isdsAppliance2)

    for obj in ret_obj1['data']['snmpObjects']:
        del obj['uuid']
    for obj in ret_obj2['data']['snmpObjects']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
