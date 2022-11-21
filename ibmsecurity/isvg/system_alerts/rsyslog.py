import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isvgAppliance, check_mode=False, force=False):
    """
    Get all rsyslog objects
    """
    return isvgAppliance.invoke_get("Get all rsyslog objects",
                                    "/rsp_rsyslog_objs")


def get(isvgAppliance, uuid, check_mode=False, force=False):
    """
    Get a specific rsyslog object
    """
    return isvgAppliance.invoke_get("Get a specific rsyslog object",
                                    "/rsp_rsyslog_objs/{0}".format(uuid))


def add(isvgAppliance, name, collector, collectorPort=514, collectorLeef=False, objType='rsyslog', comment='',
        check_mode=False, force=False):
    """
    Add a rsyslog object
    """
    if force is True or _check(isvgAppliance, None, name, objType, comment, collector, collectorPort,
                               collectorLeef) is False:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_post(
                "Add a rsyslog object",
                "/rsp_rsyslog_objs/",
                {
                    'name': name,
                    'objType': objType,
                    'comment': comment,
                    'collector': collector,
                    'collectorPort': collectorPort,
                    'collectorLeef': collectorLeef
                })

    return isvgAppliance.create_return_object()


def update(isvgAppliance, uuid, name, collector, collectorPort=514, collectorLeef=False, objType='rsyslog', comment='',
           check_mode=False, force=False):
    """
    Update a specific rsyslog object
    """
    if force is True or (
            _exists(isvgAppliance, uuid) is True and _check(isvgAppliance, uuid, name, objType, comment,
                                                            collector, collectorPort, collectorLeef) is False):
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put(
                "Update a specific rsyslog object",
                "/rsp_rsyslog_objs/{0}".format(uuid),
                {
                    'name': name,
                    'uuid': uuid,
                    'objType': objType,
                    'comment': comment,
                    'collector': collector,
                    'collectorPort': collectorPort,
                    'collectorLeef': collectorLeef
                })

    return isvgAppliance.create_return_object()


def delete(isvgAppliance, uuid, check_mode=False, force=False):
    """
    Delete a rsyslog object
    """
    if force is True or _exists(isvgAppliance, uuid) is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_delete(
                "Delete a rsyslog object",
                "/rsp_rsyslog_objs/{0}".format(uuid))

    return isvgAppliance.create_return_object()


def _exists(isvgAppliance, uuid):
    """
    Check if an uuid object exists

    :param isvgAppliance:
    :param uuid:
    :return:
    """
    exists = False
    ret_obj = get_all(isvgAppliance)

    for rsyslog in ret_obj['data']['rsyslogObjects']:
        if rsyslog['uuid'] == uuid:
            exists = True
            break

    return exists


def _check(isvgAppliance, uuid, name, objType, comment, collector, collectorPort, collectorLeef):
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

    ret_obj = get_all(isvgAppliance)
    for obj in ret_obj['data']['rsyslogObjects']:
        if uuid is None and obj['name'] == name:
            return True
        elif ibmsecurity.utilities.tools.json_sort(obj) == set_value:
            return True

    return False


def compare(isvgAppliance1, isvgAppliance2):
    """
    Compare rsyslog objects between two appliances
    """
    ret_obj1 = get_all(isvgAppliance1)
    ret_obj2 = get_all(isvgAppliance2)

    for obj in ret_obj1['data']['rsyslogObjects']:
        del obj['uuid']
    for obj in ret_obj2['data']['rsyslogObjects']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
