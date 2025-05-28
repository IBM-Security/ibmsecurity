import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get(isamAppliance, state_id, check_mode=False, force=False):
    """
    Get a grant
    """
    return isamAppliance.invoke_get("Get a grant",
                                    f"/iam/access/v8/grants/{state_id}")


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get all grants
    """
    return isamAppliance.invoke_get("Get all grants",
                                    "/iam/access/v8/grants")


def get_users(isamAppliance, sortBy=None, filter=None, check_mode=False, force=False):
    """
    Get all users that have grants
    """
    return isamAppliance.invoke_get("Get all users that have grants",
                                    f"/iam/access/v8/grants/userIds{tools.create_query_string(sortBy=sortBy, filter=filter)}")


def set(isamAppliance, state_id, attributes=[], isEnabled=True, check_mode=False,
        force=False):
    """
    Update a specified grant

    NOTE: Unable to update attributes, getting an error like so:
        {"result":"FBTRBA0100E The action: UPDATE failed because the resource [https:\/\/<hostname>:443\/iam\/access\/v8\/grants\/uuid70c19d9-0158-1c78-8de9-cb87b95521e8] was not found."}
    """
    if (isinstance(attributes, basestring)):
        import ast
        attributes = ast.literal_eval(attributes)
    if (isinstance(isEnabled, basestring)):
        import ast
        isEnabled = ast.literal_eval(isEnabled)

    if force is True or _check(isamAppliance, state_id, isEnabled, attributes) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Update a specified grant",
                                            f"/iam/access/v8/grants/{state_id}",
                                            {
                                                'isEnabled': isEnabled,
                                                'attributes': attributes
                                            })

    return isamAppliance.create_return_object()


def delete(isamAppliance, state_id, check_mode=False, force=False):
    """
    Delete a grant
    """
    if force is True or _check(isamAppliance, state_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Delete a grant",
                                               f"/iam/access/v8/grants/{state_id}")

    return isamAppliance.create_return_object()


def _check(isamAppliance, state_id, isEnabled=None, attributes=None):
    try:
        ret_obj = get(isamAppliance, state_id)
        if ret_obj['data']['id'] == state_id:
            if isEnabled is None and attributes is None:
                return True
            else:
                if ret_obj['data']['isEnabled'] != isEnabled:
                    return True
                import ibmsecurity.utilities.tools
                if ibmsecurity.utilities.tools.json_sort(
                        ret_obj['data']['attributes']) != ibmsecurity.utilities.tools.json_sort(attributes):
                    return True
    except:
        pass

    return False
