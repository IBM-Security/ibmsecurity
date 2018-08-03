import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)
module_uri = "/rsp_snmp_objs/"
requires_version = None
requires_modules = None


def get_all(isdsAppliance, check_mode=False, force=False):
    """
    Get all snmp objects
    """
    return isdsAppliance.invoke_get("Get all snmp objects",
                                    module_uri, requires_modules=requires_modules, requires_version=requires_version)


def get(isdsAppliance, name, check_mode=False, force=False):
    """
    Get a specific snmp object
    """

    ret_obj = search(isdsAppliance, name, check_mode, force)
    uuid = ret_obj['data']

    if uuid == {}:
        logger.info("Alert {0} had no match, skipping retrieval.".format(name))
        return isdsAppliance.create_return_object()
    else:
        return _get(isdsAppliance, uuid)


def _get(isdsAppliance, uuid):
    return isdsAppliance.invoke_get("Retreiving SNMP Object", "{}{}".format(module_uri, uuid))


def add(isdsAppliance, name, trapAddress, trapCommunity, trapNotificationType=None, trapVersion='V1', trapPort=162,
        objType='snmp', username=None, authEnabled=False, authType=None, authPassPhrase=None, privEnabled=None,
        privType=None, privPassPhrase=None, informSnmpEngineID=None, informTimeout=None, comment='', check_mode=False,
        force=False):
    """
    Add a snmp object
    """
    if force is False:
        ret_obj = search(isdsAppliance, name, check_mode, force)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post(
                "Add a snmp object",
                module_uri,
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
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isdsAppliance.create_return_object()


def update(isdsAppliance, name, trapAddress, trapCommunity, new_name=None, trapNotificationType=None, trapVersion='V1',
           trapPort=162, objType='snmp', username=None, authEnabled=False, authType=None, authPassPhrase=None,
           privEnabled=None, privType=None, privPassPhrase=None, informSnmpEngineID=None, informTimeout=None,
           comment='', check_mode=False, force=False):
    """
    Update a specific snmp object
    """
    uuid = search(isdsAppliance, name)['data']

    change_required, json_data = _check(isdsAppliance, name, trapAddress, trapCommunity,
                                               new_name, trapNotificationType, trapVersion, trapPort, objType,
                                               username, authEnabled, authType, authPassPhrase, privEnabled,
                                               privType, privPassPhrase, informSnmpEngineID,
                                               informTimeout, comment)

    if force is True or change_required is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_put(
                "Update a specific snmp object",
                "{}{}".format(module_uri, uuid),
                json_data, requires_modules=requires_modules, requires_version=requires_version)

    return isdsAppliance.create_return_object()


def set(isdsAppliance, name, trapAddress, trapCommunity, trapNotificationType=None, trapVersion='V1',
        trapPort=162, objType='snmp', username=None, authEnabled=False, authType=None, authPassPhrase=None,
        privEnabled=None, privType=None, privPassPhrase=None, informSnmpEngineID=None, informTimeout=None,
        comment='', check_mode=False, force=False):
    """
    set function determines if add or update is required then executes the correct function
    """
    if search(isdsAppliance, name)['data'] != {}:
        logger.info("Updating SNMP")

        return update(isdsAppliance, name, trapAddress, trapCommunity, trapNotificationType=trapNotificationType,
                      trapVersion=trapVersion,
                      trapPort=trapPort, objType=objType, username=username, authEnabled=authEnabled, authType=authType,
                      authPassPhrase=authPassPhrase, privEnabled=privEnabled, privType=privType,
                      privPassPhrase=privPassPhrase,
                      informSnmpEngineID=informSnmpEngineID, informTimeout=informTimeout, comment=comment,
                      check_mode=check_mode, force=force)
    else:
        logger.info("Adding SNMP")

        return add(isdsAppliance, name, trapAddress, trapCommunity, trapNotificationType, trapVersion, trapPort,
                   objType, username, authEnabled, authType, authPassPhrase, privEnabled, privType, privPassPhrase,
                   informSnmpEngineID, informTimeout, comment, check_mode, True)  # <--- add this everywhere


def delete(isdsAppliance, name, check_mode=False, force=False):
    """
    Delete a snmp object
    """
    ret_obj = search(isdsAppliance, name, check_mode, force)
    mech_id = ret_obj['data']

    if mech_id == {}:
        logger.info("Policy {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_delete(
                "Delete a Policy",
                "{0}{1}".format(module_uri, mech_id))

    return isdsAppliance.create_return_object()


def search(isdsAppliance, name, check_mode=False, force=False):
    """
    Search for existing object, and returning the uuid for given name.
    """
    ret_obj = get_all(isdsAppliance)
    return_obj = isdsAppliance.create_return_object()

    for obj in ret_obj['data']['snmpObjects']:
        if obj['name'] == name:
            logger.info("Found SNMP Object {0} id: {1}".format(name, obj['uuid']))
            return_obj['data'] = obj['uuid']
            return_obj['rc'] = 0

    return return_obj


def _check(isdsAppliance, name, trapAddress, trapCommunity, new_name=None, trapNotificationType=None,
                  trapVersion='V1',
                  trapPort=162, objType='snmp', username=None, authEnabled=False, authType=None, authPassPhrase=None,
                  privEnabled=None, privType=None, privPassPhrase=None, informSnmpEngineID=None, informTimeout=None,
                  comment='', check_mode=False, force=False):

    check_obj = get(isdsAppliance, name)
    change_required = False

    if new_name != None:
        name = new_name
    ret_obj = {
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
    }
    if check_obj['data'] == {}:
        logger.warning("SNMP Object not found, No update required")
        return change_required, ret_obj

    logger.debug("Check Object {0}".format(check_obj))
    del check_obj['data']['uuid']

    check_obj = ibmsecurity.utilities.tools.json_sort(check_obj['data'])
    sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj)

    logger.debug("Check Object: {}".format(check_obj))
    logger.debug("Return Object: {}".format(sorted_ret_obj))

    if check_obj != sorted_ret_obj:
        change_required = True

    return change_required, ret_obj


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
