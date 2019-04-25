import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get all rsyslog objects
    """
    return isamAppliance.invoke_get("Get all rsyslog objects",
                                    "/core/rsp_rsyslog_objs")


def get(isamAppliance, uuid, check_mode=False, force=False):
    """
    Get a specific rsyslog object
    """
    return isamAppliance.invoke_get("Get a specific rsyslog object",
                                    "/core/rsp_rsyslog_objs/{0}".format(uuid))


def add(isamAppliance, name, collector, collectorPort=514, collectorLeef=False, objType='rsyslog', comment='',
        check_mode=False, force=False):
    """
    Add a rsyslog object
    """
    if force is True or _check(isamAppliance, None, name, objType, comment, collector, collectorPort,
                               collectorLeef) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add a rsyslog object",
                "/core/rsp_rsyslog_objs/",
                {
                    'name': name,
                    'objType': objType,
                    'comment': comment,
                    'collector': collector,
                    'collectorPort': collectorPort,
                    'collectorLeef': collectorLeef
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, uuid, name, collector, collectorPort=514, collectorLeef=False, objType='rsyslog', comment='',
           check_mode=False, force=False):
    """
    Update a specific rsyslog object
    """
    if force is True or (
            _exists(isamAppliance, uuid) is True and _check(isamAppliance, uuid, name, objType, comment,
                                                            collector, collectorPort, collectorLeef) is False):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specific rsyslog object",
                "/core/rsp_rsyslog_objs/{0}".format(uuid),
                {
                    'name': name,
                    'uuid': uuid,
                    'objType': objType,
                    'comment': comment,
                    'collector': collector,
                    'collectorPort': collectorPort,
                    'collectorLeef': collectorLeef
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, uuid, check_mode=False, force=False):
    """
    Delete a rsyslog object
    """
    if force is True or _exists(isamAppliance, uuid) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a rsyslog object",
                "/core/rsp_rsyslog_objs/{0}".format(uuid))

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

    for rsyslog in ret_obj['data']['rsyslogObjects']:
        if rsyslog['uuid'] == uuid:
            exists = True
            break

    return exists


def _check(isamAppliance, uuid, name, objType, comment, collector, collectorPort, collectorLeef):
    """
    Check if the rsyslog object exists and is the same - uuid=None means add versus delete

    NOTE: if UUID is not found that will be same as no match!!!
    """

    set_value = {
        'name': name,
        'uuid': uuid,
        'objType': objType,
        'comment': comment,
        'collector': collector,
        'collectorPort': collectorPort,
        'collectorLeef': collectorLeef
    }

    set_value = ibmsecurity.utilities.tools.json_sort(set_value)

    ret_obj = get_all(isamAppliance)
    for obj in ret_obj['data']['rsyslogObjects']:
        if uuid is None and obj['name'] == name:
            return True
        elif ibmsecurity.utilities.tools.json_sort(obj) == set_value:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare rsyslog objects between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']['rsyslogObjects']:
        del obj['uuid']
    for obj in ret_obj2['data']['rsyslogObjects']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
