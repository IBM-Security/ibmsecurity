import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get management authorization - roles
    """
    return isamAppliance.invoke_get("Get management authorization - roles",
                                    "/authorization/roles/v1")


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Get management authorization role
    """
    return isamAppliance.invoke_get("Get management authorization role",
                                    "/authorization/roles/{0}/v1".format(name))


def _check(isamAppliance, name):
    """
    Check if management authorization role exists
    """
    ret_obj = get_all(isamAppliance)

    for role in ret_obj['data']:
        if role['name'] == name:
            return True

    return False


def add(isamAppliance, name, check_mode=False, force=False):
    """
    Add a management authorization role
    """
    if force is True or _check(isamAppliance, name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Add management authorization role",
                                             "/authorization/roles/v1",
                                             {
                                                 'name': name,
                                                 'users': None,
                                                 'groups': None,
                                                 'features': None
                                             })

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a management authorization role
    """
    if force is True or _check(isamAppliance, name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete management authorization role",
                "/authorization/roles/{0}/v1".format(name))

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare all management authorization roles
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
