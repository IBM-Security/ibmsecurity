import logging

logger = logging.getLogger(__name__)

uri = "/mga/user_registry/groups"
requires_modules = ["mga", "federation"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all current groups in the registry
    """
    return isamAppliance.invoke_get("Retrieving a list of all current groups in the registry",
                                    "{0}/v1".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieving details for a particular group in the registry
    """
    return isamAppliance.invoke_get("Retrieving details for a particular group in the registry",
                                    "{0}/{1}/v1".format(uri, id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def add_user(isamAppliance, user_name, id, check_mode=False, force=False):
    """
    Adding a user to a group in the registry
    """
    if force is True or _check(isamAppliance, user_name, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Adding a user to a group in the registry",
                "/mga/user_registry/users/{0}/groups/v1".format(user_name),
                {
                    'id': id
                },
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete_user(isamAppliance, user_name, id, check_mode=False, force=False):
    """
    Removing a user from a group in the registry
    """
    if force is True or _check(isamAppliance, user_name, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Removing a user from a group in the registry",
                "/mga/user_registry/users/{0}/groups/{1}/v1".format(user_name, id),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, user_name, id):
    """
    Check if user already exists
    """
    ret_obj = get_all(isamAppliance)

    for grp in ret_obj['data']:
        if grp['id'] == id:
            ret_obj = get(isamAppliance, id)
            for usr in ret_obj['data']['users']:
                if usr['id'] == user_name:
                    return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare groups between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        user = get(isamAppliance1, obj['id'])
        obj['users'] = user['data']['users']
    for obj in ret_obj2['data']:
        user = get(isamAppliance2, obj['id'])
        obj['users'] = user['data']['users']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[''])
