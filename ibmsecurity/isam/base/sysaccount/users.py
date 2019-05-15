import logging
import ibmsecurity.utilities.tools
import os.path

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get information on existing users
    """
    return isamAppliance.invoke_get("Retrieving users", "/sysaccount/users/v1")


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Get information on particular user by id
    """
    return isamAppliance.invoke_get("Retrieving user", "/sysaccount/users/{0}/v1".format(id))


def create(isamAppliance, id, password, groups=[], check_mode=False, force=False):
    """
    Create a new user
    """
    if force is True or _check(isamAppliance, id=id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Creating user", "/sysaccount/users/v1",
                                             {
                                                 'id': id,
                                                 'password': password,
                                                 'groups': groups
                                             })

    return isamAppliance.create_return_object()


def _check(isamAppliance, id=None):
    """
    Check if the last created user has the exact same id or id exists

    :param isamAppliance:
    :param comment:
    :return:
    """
    ret_obj = get_all(isamAppliance)

    if id != None:
        for users in ret_obj['data']:
            if users['id'] == id:
                return True

    return False


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Delete a user
    """
    if force is True or _check(isamAppliance, id=id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting user", "/sysaccount/users/{0}/v1".format(id))

    return isamAppliance.create_return_object()


def modify(isamAppliance, id, password, old_password=None, check_mode=False, force=False):
    """
    Change a users password
    """
    warnings = []
    if old_password is not None and old_password != '':
        warnings.append("old_password is not required. Provided value will be ignored.")
    if force is True or _check(isamAppliance, id=id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Change password", "/sysaccount/users/{0}/v1".format(id),
                                            {
                                                'password': password
                                            }, warnings=warnings)

    return isamAppliance.create_return_object()


def modify_self(isamAppliance, password, old_password, check_mode=False, force=False):
    """
    Change the current user's password
    """
    if force is True or password != old_password:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Change password", "/sysaccount/self/v1",
                                            {
                                                'password': password,
                                                'old_password': old_password
                                            })

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare the list of users between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
