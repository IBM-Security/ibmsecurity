import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)
module_uri = "/rsp_email_objs/"
requires_version = None
requires_modules = None


def get_all(isdsAppliance, check_mode=False, force=False):
    """
    Get all email objects
    """
    return isdsAppliance.invoke_get("Get all email objects",
                                    module_uri, requires_modules=requires_modules, requires_version=requires_version)


def get(isdsAppliance, name, check_mode=False, force=False):
    """
    Get a specific email object
    """
    ret_obj = search(isdsAppliance, name=name, check_mode=check_mode, force=force)
    obj_id = ret_obj['data']

    if obj_id == {}:
        logger.info("Object {0} had no match, skipping retrieval.".format(name))
        return isdsAppliance.create_return_object()
    else:
        return _get(isdsAppliance, obj_id)


def _get(isdsAppliance, uuid):
    return isdsAppliance.invoke_get("Get a specific email object",
                                    "{0}{1}".format(module_uri, uuid), requires_modules=requires_modules,
                                    requires_version=requires_version)


def add(isdsAppliance, name, smtpServer, from_email, to_email, smtpPort=25, objType='email',
        comment=None, check_mode=False, force=False):
    """
    Add an email object
    """
    if force is False:
        ret_obj = search(isdsAppliance, name, check_mode, force)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post(
                "Add an email object",
                module_uri,
                {
                    'name': name,
                    'objType': objType,
                    'comment': comment,
                    'smtpServer': smtpServer,
                    'smtpPort': smtpPort,
                    'from': from_email,
                    'to': to_email
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isdsAppliance.create_return_object()


def update(isdsAppliance, name, smtpServer, from_email, to_email, new_name=None, smtpPort=25, objType='email',
           comment='', check_mode=False, force=False):
    """
    Update a specific email object
    """
    change_required, json_data = _check(isdsAppliance, name, smtpServer, from_email, to_email, new_name, smtpPort,
                                        objType, comment)
    uuid = search(isdsAppliance, name)['data']

    if force is True or change_required is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_put(
                "Update a specific email object",
                "{0}{1}".format(module_uri, uuid),
                {
                    'name': name,
                    'objType': objType,
                    'comment': comment,
                    'smtpServer': smtpServer,
                    'smtpPort': smtpPort,
                    'from': from_email,
                    'to': to_email
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isdsAppliance.create_return_object()


def set(isdsAppliance, name, smtpServer, from_email, to_email, smtpPort=25, objType='email',
        comment='', check_mode=False, force=False):
    """
    determines if add or update is executed
    """

    if _exists(isdsAppliance, search(isdsAppliance, name)) is True:

        logger.info("Updating SMTP")
        return update(isdsAppliance, name, smtpServer, from_email, to_email, smtpPort, objType, comment,
                      check_mode, force)
    else:
        logger.info("Adding SMTP")
        return add(isdsAppliance, name, smtpServer, from_email, to_email, smtpPort, objType,
                   comment, check_mode, True)


def delete(isdsAppliance, name, check_mode=False, force=False):
    """
    Delete an email object
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


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search policy id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']['emailObjects']:
        if obj['name'] == name:
            logger.info("Found Email Object {0} id: {1}".format(name, obj['uuid']))
            return_obj['data'] = obj['uuid']
            return_obj['rc'] = 0

    return return_obj


def _check(isdsAppliance, name, smtpServer, from_email, to_email, new_name, smtpPort, objType,
           comment):
    """
    Check if the email object exists and is the same
    """
    check_obj = get(isdsAppliance, name)
    change_required = False

    if new_name != None:
        name = new_name

    ret_obj = {
        'name': name,
        'comment': comment,
        'objType': objType,
        'smtpServer': smtpServer,
        'smtpPort': smtpPort,
        'from': from_email,
        'to': to_email
    }

    if check_obj['data'] == {}:
        logger.warning("Email Object not found, No update required")
        return change_required, ret_obj

    del check_obj['data']['uuid']

    sorted_check_obj = ibmsecurity.utilities.tools.json_sort(check_obj['data'])
    sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj)

    logger.debug("Check Object: {}".format(sorted_check_obj))
    logger.debug("Return Object: {}".format(ret_obj))

    if sorted_ret_obj != sorted_check_obj:
        change_required = True

    return change_required, ret_obj


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare email objects between two appliances
    """
    ret_obj1 = get_all(isdsAppliance1)
    ret_obj2 = get_all(isdsAppliance2)

    for obj in ret_obj1['data']['emailObjects']:
        del obj['uuid']
    for obj in ret_obj2['data']['emailObjects']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
