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
    return isamAppliance.invoke_get("Retrieving key", f"/admin_cfg/ssh-keys/{uuid}/v1")


def add(isamAppliance, key, name, check_mode=False, force=False):
    """
    Import ssh public key for the default admin user
    """
    if force or not _check(isamAppliance, name):
        if check_mode:
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

create = add
def update(isamAppliance, key, name, check_mode=False, force=False):
    """
    Update an existing key
    """
    # We know we need to do an update.  The only thing we can verify is that the comment is part
    update_required = True
    ret_obj = get(isamAppliance, name)
    if not ret_obj:
        # means we cannot find the name
        logger.debug("Cannot find sshkeys by name")
        update_required = False
    elif key:
        # Extract the comment from the new ssh public key
        key_comment = key.split(' ')[-1]
        logger.debug(f"See if {key_comment} for admin exists in a key")
        if key_comment in ret_obj['data']['fingerprint']:
            update_required = False

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True, warnings=warnings)
    elif update_required:
        delete(isamAppliance, name)
        return add(isamAppliance, key, name)

    return isamAppliance.create_return_object()

def set(isamAppliance, key, name, fingerprint=None, check_mode=False, force=False):
    """
    Create key if it does not exist yet, update if it does.

    The fingerprint is the output format of ssh-keygen:  `ssh-keygen -l -f ~/.ssh/id_rsa.pub`
    It is NOT used to send to ISVA, it is used to check if a key already exists.
    """
    if not _check(isamAppliance, name, fingerprint):
        # Force the add - we already know there is no key by this name or fingerprint
        return add(isamAppliance, key=key, name=name,
                   check_mode=check_mode, force=True)
    else:
        # There is no update.  Let's see what this does.
        return update(isamAppliance, key=key, name=name, check_mode=check_mode, force=force)


def _check(isamAppliance, name=None, fingerprint=None):
    """
    The fingerprint is generated from the actual public key, using `ssh-keygen -l -f ~/.ssh/id_rsa.pub`
    I'm unsure how to do this in Python, but I'm adding it to the check anyway (because Ansible)

    If a fingerprint is supplied, that is the only parameter that will be used.
    The only way to have full idempotency, is by having the fingerprint.

    The other checks will not be completely idempotent.

    :param isamAppliance:
    :param name:
    :return:
    """
    ret_obj = get_all(isamAppliance)
    # Fingerprint rules
    if fingerprint:
        for sshkeys in ret_obj['data']:
            if sshkeys.get('fingerprint') == fingerprint:
                logger.debug(f"Fingerprint matched on {sshkeys.get('name')} for the admin user")
                return True

    if name:
        for sshkeys in ret_obj['data']:
            if sshkeys.get('name') == name:
                logger.debug(f"Name found on {sshkeys.get('name')} for the admin user")
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
