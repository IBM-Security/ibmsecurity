import logging
import ibmsecurity.utilities.tools
import json

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
                                    f"/authorization/roles/{name}/v1")


def _check(isamAppliance, name):
    """
    Check if management authorization role exists
    """
    ret_obj = get_all(isamAppliance)

    for role in ret_obj['data']:
        if role['name'] == name:
            return True

    return False

def add(isamAppliance, name, users=None, groups=None, features=None, check_mode=False, force=False):
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
                                                 'users': users,
                                                 'groups': groups,
                                                 'features': features
                                             })

    return isamAppliance.create_return_object()

def set(isamAppliance, name, users=None, groups=None, features=None, check_mode=False, force=False):
    """
    Configure a management authorization role
    """
    if _check(isamAppliance, name):
        # Update request
        return update(isamAppliance, name, users, groups, features, check_mode, force)
    else:
        # Force the add - we already know connection does not exist
        return add(isamAppliance, name, users, groups, features, check_mode, force)

def update(isamAppliance, name, users=None, groups=None, features=None, check_mode=False, force=False):
    """
    Update an existing management authorization role
    """
    _performUpdate = False
    if check_mode:
        return isamAppliance.create_return_object(changed=True)

    if force:
        _performUpdate = True
    else:
        """
        Compare
        """
        ret_obj = get(isamAppliance, name)
        newEntries = {
                      'name': name,
                      'users': users,
                      'groups': groups,
                      'features': features
                     }
        newEntriesJSON = json.dumps(newEntries, skipkeys=True, sort_keys=True)
        logger.debug(f"\nSorted management role configuration {name}:\n\n {newEntriesJSON}\n")
        currentEntriesJSON = json.dumps(ret_obj['data'], skipkeys=True, sort_keys=True)
        logger.debug(f"\nSorted Existing management role configuration {name}:\n\n {currentEntriesJSON}\n")
        if (newEntriesJSON != currentEntriesJSON):
            _performUpdate = True
    if not _performUpdate:
        logger.debug(f"No changes to role {name}")
        return isamAppliance.create_return_object(changed=False)
    else:
        return isamAppliance.invoke_put("Set management authorization role",
                                     f"/authorization/roles/{name}/v1", newEntries)

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
                f"/authorization/roles/{name}/v1")

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare all management authorization roles
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
