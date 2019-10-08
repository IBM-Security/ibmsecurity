import logging

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)

uri = "/mga/user_registry/users"
requires_modules = ["mga", "federation"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all current users in the registry
    """
    return isamAppliance.invoke_get("Retrieving a list of all current users in the registry",
                                    "{0}/v1".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieving details for a particular user in the registry
    """
    return isamAppliance.invoke_get("Retrieving details for a particular user in the registry",
                                    "{0}/{1}/v1".format(uri, id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def add(isamAppliance, id, password, groups=None, check_mode=False, force=False):
    """
    Creating a new user in the registry
    """
    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "id": id,
                "password": password
            }
            if groups is not None:
                if isinstance(groups, basestring):
                    import ast
                    groups = ast.literal_eval(groups)
                json_data['groups'] = groups
            return isamAppliance.invoke_post(
                "Creating a new user in the registry",
                "{0}/v1".format(uri), json_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting a user in the registry
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a user in the registry",
                "{0}/{1}/v1".format(uri, id),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def set_pw(isamAppliance, id, password, check_mode=False, force=False):
    """
    Changing the password of a user in the registry
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Changing the password of a user in the registry",
            "{0}/{1}/v1".format(uri, id),
            {
                'password': password
            },
            requires_modules=requires_modules, requires_version=requires_version)


def _check(isamAppliance, id):
    """
    Check if user already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['id'] == id:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Users between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        user = get(isamAppliance1, obj['id'])
        obj['groups'] = user['data']['groups']
    for obj in ret_obj2['data']:
        user = get(isamAppliance2, obj['id'])
        obj['groups'] = user['data']['groups']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[''])
