import logging
import ibmsecurity.utilities.tools
from ibmsecurity.appliance.ibmappliance import IBMError

logger = logging.getLogger(__name__)

requires_modules = ["wga"]
requires_version = "10.0.6.0"

def get_all(isamAppliance, user, check_mode=False, force=False):
    """
    Get all SSH keys for a user
    """
    return isamAppliance.invoke_get("Retrieving keys", f"/sysaccount/users/{user}/ssh-keys/v1")


def get(isamAppliance, user, name=None, uuid=None, check_mode=False, force=False):
    """
    Get specific ssh key for a user

    """
    if uuid is not None and name is None:
        return isamAppliance.invoke_get("Retrieving key", f"/sysaccount/users/{user}/ssh-keys/{uuid}/v1")
    elif name is not None and uuid is None:
        # Get the key based on the name
        allKeys = get_all(isamAppliance, user)
        logger.debug(allKeys.get('data'))
        uuids = [d.get('uuid') for d in allKeys.get('data') if d['name'] == name]
        # I expect we'll have 0 or 1 results now
        if uuids:
            uuid = uuids[0]
            return isamAppliance.invoke_get("Retrieving key", f"/sysaccount/users/{user}/ssh-keys/{uuid}/v1")
        else:
            return None
    else:
        # Input error
        raise IBMError("999", "Cannot get the ssh keys.  Provide exactly 1 of the parameters uuid or name")

def add(isamAppliance, user, key, name, check_mode=False, force=False):
    """
    Import ssh key
    """
    if force or not _check(isamAppliance, user, name=name):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "Import ssh key",
                f"/core/sysaccount/users/{user}/ssh-keys/v1",
                    {
                        'key': key,
                        'name': name
                    })

    return isamAppliance.create_return_object()

# alias for function add
create = add
def update(isamAppliance, user, key, name, check_mode=False, force=False):
    """
    Update an existing key
    """
    # We know we need to do an update.  The only thing we can verify is that the comment is part
    update_required = True
    ret_obj = get(isamAppliance, user, name)
    warnings = []
    if not ret_obj:
        # means we cannot find the name
        logger.debug(f"Cannot find sshkeys by name ({name}).  This happens when we had a match on fingerprint (not on name)")
        warnings.append(f"This public key ({name}) is already there by another name.")
        update_required = False
    elif key:
        # Extract the comment from the new ssh public key
        key_comment = key.split(' ')[-1]
        logger.debug(f"See if {key_comment} for {user} is in an existing key")
        if key_comment in ret_obj['data']['fingerprint']:
            update_required = False

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True, warnings=warnings)
    elif update_required:
        delete(isamAppliance, user, name)
        return add(isamAppliance, user, key, name)

    return isamAppliance.create_return_object(warnings=warnings)

def set(isamAppliance, user, key, name, fingerprint=None, check_mode=False, force=False):
    """
    Create key if it does not exist yet, update if it does.

    The fingerprint is the output format of ssh-keygen:  `ssh-keygen -l -f ~/.ssh/id_rsa.pub`
    It is NOT used to send to ISVA, it is used to check if a key already exists.
    """
    if not _check(isamAppliance, user, name, fingerprint):
        # Force the add - we already know there is no key by this name or fingerprint
        return add(isamAppliance, user, key, name,
                   check_mode=check_mode, force=True)
    else:
        # There is no update.  Let's see what this does.
        return update(isamAppliance, user=user, key=key, name=name, check_mode=check_mode, force=force)

def _check(isamAppliance, user=None, name=None, fingerprint=None):
    """
    The fingerprint is generated from the actual public key, using `ssh-keygen -l -f ~/.ssh/id_rsa.pub`
    I'm unsure how to do this in Python, but I'm adding it to the check anyway (because Ansible)

    If a fingerprint is supplied, that is the only parameter that will be used.
    The only way to have full idempotency, is by having the fingerprint.

    The other checks will not be completely idempotent.

    :param isamAppliance:
    :param user:
    :param name:
    :return:
    """
    ret_obj = get_all(isamAppliance, user)
    # Fingerprint rules
    if fingerprint:
        for sshkeys in ret_obj['data']:
            logger.debug(sshkeys.get('fingerprint'))
            if sshkeys.get('fingerprint') == fingerprint:
                logger.debug(f"Fingerprint matched on {sshkeys.get('name')} for {user}")
                return True

    if name:
        for sshkeys in ret_obj['data']:
            if sshkeys.get('name') == name:
                logger.debug(f"Name found on {sshkeys.get('name')} for {user}")
                return True
    return False


def delete(isamAppliance, user, name=None, uuid=None, check_mode=False, force=False):
    """
    Delete a ssh_key
    """
    ret_obj = get(isamAppliance, user, name, uuid)

    if force or ret_obj.get('data'):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if not uuid:
                uuid = ret_obj.get('data').get('uuid')
            return isamAppliance.invoke_delete("Deleting key",
                f"/sysaccount/users/{user}/ssh-keys/{uuid}/v1")

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare the list of users between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
