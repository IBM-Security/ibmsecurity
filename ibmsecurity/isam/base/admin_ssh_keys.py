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


def get(isamAppliance, name=None, uuid=None, check_mode=False, force=False):
    """
    Get specific ssh key for admin user

    """
    if uuid is not None and name is None:
        return isamAppliance.invoke_get("Retrieving key", f"/admin_cfg/ssh-keys/{uuid}/v1")
    elif name is not None and uuid is None:
        # Get the key based on the name
        allKeys = get_all(isamAppliance)
        logger.debug(allKeys.get('data'))
        uuids = [d.get('uuid') for d in allKeys.get('data') if d['name'] == name]
        # I expect we'll have 0 or 1 results now
        if uuids:
            uuid = uuids[0]
            return isamAppliance.invoke_get("Retrieving key", f"/admin_cfg/ssh-keys/{uuid}/v1")
        else:
            return None
    else:
        # Input error
        raise IBMError("999", "Cannot get the ssh keys for the administrator. Provide exactly 1 of the parameters uuid or name")


def add(isamAppliance, key=None, name=None, check_mode=False, force=False):
    """
    Import ssh public key for the default admin user
    """
    warnings = []
    if force or not _check(isamAppliance, name):
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            retObj = isamAppliance.invoke_post(
                "Import ssh key",
                "/admin_cfg/ssh-keys/v1",
                    {
                        'key': key,
                        'name': name
                    },
                ignore_error=True),

            # On error 400, this message: A SSH Key with this fingerprint already exists.

            logger.debug(retObj)

            if retObj[0].get('rc', -1) == 400:
               warnings.append(f"{retObj[0].get('data', {}).get('message', 'unknown error')}")

    return isamAppliance.create_return_object(warnings=warnings)

create = add
def update(isamAppliance, key=None, name=None, check_mode=False, force=False):
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

def set(isamAppliance, key=None, name=None, fingerprint=None, check_mode=False, force=False):
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


def delete(isamAppliance, name=None, uuid=None, check_mode=False, force=False):
    """
    Delete a public ssh_key for the default admin user
    """
    ret_obj = get(isamAppliance, name, uuid)
    if force or ret_obj.get('data'):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if not uuid:
                uuid = ret_obj.get('data').get('uuid')
            return isamAppliance.invoke_delete("Deleting key",
                                               f"/admin_cfg/ssh-keys/{uuid}/v1")

    return isamAppliance.create_return_object()

def compare(isamAppliance1, isamAppliance2):
    """
    Compare the list of SSH keys between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
