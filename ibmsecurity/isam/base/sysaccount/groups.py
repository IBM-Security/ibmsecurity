import logging
import ibmsecurity.utilities.tools
import os.path

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get information on existing groups
    """
    return isamAppliance.invoke_get("Retrieving groups", "/sysaccount/groups/v1")


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Get information on particular group by id
    """
    return isamAppliance.invoke_get("Retrieving group", "/sysaccount/groups/{0}/v1".format(id))


def create(isamAppliance, id, check_mode=False, force=False):
    """
    Create a new group
    """
    if force is True or _check(isamAppliance, id=id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Creating group", "/sysaccount/groups/v1",
                                             {
                                                 'id': id
                                             })

    return isamAppliance.create_return_object()


def _check(isamAppliance, id=None):
    """
    Check if the last created group has the exact same id or id exists

    :param isamAppliance:
    :param comment:
    :return:
    """
    ret_obj = get_all(isamAppliance)

    if id != None:
        for groups in ret_obj['data']:
            if groups['id'] == id:
                return True

    return False


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Delete a group
    """
    if force is True or _check(isamAppliance, id=id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting group", "/sysaccount/groups/{0}/v1".format(id))

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare the list of groups between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
