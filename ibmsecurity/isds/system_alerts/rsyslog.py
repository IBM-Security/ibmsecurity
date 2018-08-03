import logging
import ibmsecurity.utilities.tools

module_uri = "/rsp_rsyslog_objs/"
requires_version = None
requires_modules = None

logger = logging.getLogger(__name__)


def get_all(isdsAppliance, check_mode=False, force=False):
    """
    Get all rsyslog objects
    """
    return isdsAppliance.invoke_get("Get all rsyslog objects",
                                    module_uri)


def get(isdsAppliance, name, check_mode=False, force=False):
    """
    Get a specific rsyslog object
    """

    ret_obj = search(isdsAppliance, name=name, check_mode=check_mode, force=force)
    obj_id = ret_obj['data']

    if obj_id == {}:
        logger.info("Object {0} had no match, skipping retrieval.".format(name))
        return isdsAppliance.create_return_object()
    else:
        return _get(isdsAppliance, obj_id)


def _get(isdsAppliance, uuid):
    return isdsAppliance.invoke_get("Retrieving Rsyslog Object", "{}{}".format(module_uri, uuid))


def add(isdsAppliance, name, collector, collectorPort=514, collectorLeef=False, objType='rsyslog', comment='',
        check_mode=False, force=False):
    """
    Add a rsyslog object
    """
    if force is False:
        ret_obj = search(isdsAppliance, name, check_mode, force)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post("Add a rsyslog object", module_uri,
                                             {
                                                 'name': name,
                                                 'objType': objType,
                                                 'comment': comment,
                                                 'collector': collector,
                                                 'collectorPort': collectorPort,
                                                 'collectorLeef': collectorLeef
                                             }, requires_modules=requires_modules, requires_version=requires_version)

    return isdsAppliance.create_return_object()


def update(isdsAppliance, name, collector, collectorPort=514, collectorLeef=False, objType='rsyslog', comment='',
           new_name=None,
           check_mode=False, force=False):
    """
    Update a specific rsyslog object
    """

    change_required, json_data = _check(isdsAppliance, name, collector, collectorPort, collectorLeef, objType, comment)
    uuid = search(isdsAppliance, name, check_mode, force)['data']

    if force is True or change_required is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_put(
                "Update a specific rsyslog object",
                "{}{}".format(module_uri, uuid),
                json_data, requires_modules=requires_modules, requires_version=requires_version)

    return isdsAppliance.create_return_object()


def set(isdsAppliance, name, collector, uuid=None, collectorPort=514, collectorLeef=False, objType='rsyslog',
        comment='',
        check_mode=False, force=False):
    """
    Determines if add or update is executed
    """
    if search(isdsAppliance, name, check_mode, force) != {}:
        logger.info("Updating RSYSLOG")

        return update(isdsAppliance, uuid, name, collector, collectorPort, collectorLeef, objType, comment,
                      check_mode, force)

    else:
        logger.info("Adding RSYSLOG")

        return add(isdsAppliance, name, collector, collectorPort, collectorLeef, objType, comment,
                   check_mode, True)


def delete(isdsAppliance, name, check_mode=False, force=False):
    """
    Delete a rsyslog object
    """
    ret_obj = search(isdsAppliance, name, check_mode, force)
    mech_id = ret_obj['data']

    if mech_id == {}:
        logger.info("Alert {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_delete(
                "Delete a Alert",
                "{0}{1}".format(module_uri, mech_id))

    return isdsAppliance.create_return_object()


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search alert id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']['rsyslogObjects']:
        if obj['name'] == name:
            logger.info("Found rsyslog Object {0} id: {1}".format(name, obj['uuid']))
            return_obj['data'] = obj['uuid']
            return_obj['rc'] = 0

    return return_obj


def _check(isdsAppliance, name, collector, collectorPort, collectorLeef, objType, comment, new_name=None):
    """
    Check if the rsyslog object exists and is the same - uuid=None means add versus delete

    NOTE: if UUID is not found that will be same as no match!!!
    """
    check_obj = get(isdsAppliance, name)
    change_required = False

    if new_name != None:
        name = new_name
    ret_obj = {
        'name': name,
        'objType': objType,
        'comment': comment,
        'collector': collector,
        'collectorPort': collectorPort,
        'collectorLeef': collectorLeef
    }

    if check_obj['data'] == {}:
        logger.warning("RSYSLOG Object not found, No update required")
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
    Compare rsyslog objects between two appliances
    """
    ret_obj1 = get_all(isdsAppliance1)
    ret_obj2 = get_all(isdsAppliance2)

    for obj in ret_obj1['data']['rsyslogObjects']:
        del obj['uuid']
    for obj in ret_obj2['data']['rsyslogObjects']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
