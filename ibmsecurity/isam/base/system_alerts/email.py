import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get all email objects
    """
    return isamAppliance.invoke_get("Get all email objects",
                                    "/core/rsp_email_objs")


def get(isamAppliance, uuid, check_mode=False, force=False):
    """
    Get a specific email object
    """
    return isamAppliance.invoke_get("Get a specific email object",
                                    "/core/rsp_email_objs/{0}".format(uuid))


def add(isamAppliance, name, smtpServer, from_email, to_email, smtpPort=25, objType='email',
        comment='', check_mode=False, force=False):
    """
    Add an email object
    """
    if force is True or _check(isamAppliance, None, name, comment, smtpServer, smtpPort, from_email, to_email) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add an email object",
                "/core/rsp_email_objs/",
                {
                    'name': name,
                    'objType': objType,
                    'comment': comment,
                    'smtpServer': smtpServer,
                    'smtpPort': smtpPort,
                    'from': from_email,
                    'to': to_email
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, uuid, name, smtpServer, from_email, to_email, smtpPort=25, objType='email',
           comment='', check_mode=False, force=False):
    """
    Update a specific email object
    """
    if force is True or (
            _exists(isamAppliance, uuid) is True and _check(isamAppliance, uuid, name, comment, smtpServer,
                                                            smtpPort,
                                                            from_email, to_email) is False):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specific email object",
                "/core/rsp_email_objs/{0}".format(uuid),
                {
                    'name': name,
                    'uuid': uuid,
                    'objType': objType,
                    'comment': comment,
                    'smtpServer': smtpServer,
                    'smtpPort': smtpPort,
                    'from': from_email,
                    'to': to_email
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, uuid, check_mode=False, force=False):
    """
    Delete an email object
    """
    if force is True or _exists(isamAppliance, uuid) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete an email object",
                "/core/rsp_email_objs/{0}".format(uuid))

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

    for email in ret_obj['data']['emailObjects']:
        if email['uuid'] == uuid:
            exists = True
            break

    return exists


def _check(isamAppliance, uuid, name, comment, smtpServer, smtpPort, from_email, to_email):
    """
    Check if the email object exists and is the same - uuid=None means add versus delete

    NOTE: if UUID is not found that will be same as no match!!!
    """

    set_value = {
        'name': name,
        'comment': comment,
        'objType': 'email',
        'uuid': uuid,
        'smtpServer': smtpServer,
        'smtpPort': smtpPort,
        'from': from_email,
        'to': to_email
    }

    set_value = ibmsecurity.utilities.tools.json_sort(set_value)

    ret_obj = get_all(isamAppliance)
    for obj in ret_obj['data']['emailObjects']:
        if uuid is None and obj['name'] == name:
            return True
        elif ibmsecurity.utilities.tools.json_sort(obj) == set_value:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare email objects between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']['emailObjects']:
        del obj['uuid']
    for obj in ret_obj2['data']['emailObjects']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
