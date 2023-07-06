import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

requires_modules = ["wga"]
requires_version = "10.0.6.0"

def get_all(isamAppliance, user, check_mode=False, force=False):
    """
    Get all SSH keys for a user
    """
    return isamAppliance.invoke_get("Retrieving keys", "/sysaccount/users/{0}/ssh-keys/v1".format(user))


def get(isamAppliance, user, uuid, check_mode=False, force=False):
    """
    Get specific ssh key for a user
    """
    return isamAppliance.invoke_get("Retrieving user", "/sysaccount/users/{0}/ssh-keys/{1}/v1".format(user, uuid))


def create(isamAppliance, user, key, name, check_mode=False, force=False):
    """
    Import ssh key
    """
    if force is True or _check(isamAppliance, user, key) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "Import ssh key",
                "/core/sysaccount/users/{0}/ssh-keys/v1".format(user),
                    {
                        'key': key,
                        'name': name
                    })

    return isamAppliance.create_return_object()


def _check(isamAppliance, user=None, uuid=None):
    """
    Check if the last created key has the exact same uuid or uuid exists

    :param isamAppliance:
    :param comment:
    :return:
    """
    ret_obj = get_all(isamAppliance, user)

    if uuid != None:
        for users in ret_obj['data']:
            if users['uuid'] == uuid:
                return True

    return False


def delete(isamAppliance, user, uuid, check_mode=False, force=False):
    """
    Delete a ssh_key
    """
    if force is True or _check(isamAppliance, user, uuid=uuid) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting key",
            "/sysaccount/users/{0}/ssh-keys/{1}/v1".format(user, uuid))

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare the list of users between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
