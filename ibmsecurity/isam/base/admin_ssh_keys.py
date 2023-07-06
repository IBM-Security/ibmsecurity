import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

requires_modules = ["wga"]
requires_version = "10.0.6.0"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get all SSH public keys for the default admin user
    """
    return isamAppliance.invoke_get("Retrieving keys", "/admin_cfg/ssh-keys/v1")


def get(isamAppliance, uuid, check_mode=False, force=False):
    """
    Get specific ssh public key for the default admin user
    """
    return isamAppliance.invoke_get("Retrieving key", "/admin_cfg/ssh-keys/{0}/v1".format(uuid))


def create(isamAppliance, key, name, check_mode=False, force=False):
    """
    Import ssh public key for the default admin user
    """
    if force is True or _check(isamAppliance) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "Import ssh key",
                "/admin_cfg/ssh-keys/v1",
                    {
                        'key': key,
                        'name': name
                    })

    return isamAppliance.create_return_object()


def _check(isamAppliance, uuid=None):
    """
    Check if the last created key has the exact same uuid or uuid exists

    :param isamAppliance:
    :param comment:
    :return:
    """
    ret_obj = get_all(isamAppliance)

    if uuid != None:
        for name in ret_obj['data']:
            if name['uuid'] == uuid:
                return True

    return False


def delete(isamAppliance, uuid, check_mode=False, force=False):
    """
    Delete a public ssh_key for the default admin user
    """
    if force is True or _check(isamAppliance, uuid=uuid) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting key",
            "/admin_cfg/ssh-keys/{0}/v1".format(uuid))

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare the list of SSH keys between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
