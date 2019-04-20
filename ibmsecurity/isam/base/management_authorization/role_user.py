import logging
import ibmsecurity.isam.base.management_authorization.role

logger = logging.getLogger(__name__)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieving the list of users for an authorization roles
    """
    return isamAppliance.invoke_get("Retrieving the list of users for an authorization roles",
                                    "/authorization/roles/{0}/users/v1".format(name))


def set(isamAppliance, name, user_name, type='embedded_ldap', check_mode=False, force=False):
    """
    Add a user to management authorization role
    """
    new_user = True
    ret_obj = ibmsecurity.isam.base.management_authorization.role.get(isamAppliance, name)

    if (ret_obj['data']['users'] == None):
        ret_obj['data']['users'] = []
    else:
        for usr in ret_obj['data']['users']:
            if usr['name'] == user_name:
                if usr['type'] == type:
                    if force is False:
                        return isamAppliance.create_return_object()
                    new_user = False
                else:  # Replace user with new type
                    ret_obj['data']['users'].remove(usr)
                break

    if new_user is True:
        ret_obj['data']['users'].append({'name': user_name, 'type': type})

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Add user to management authorization role",
            "/authorization/roles/{0}/v1".format(name), ret_obj['data'])


def delete(isamAppliance, name, user_name, check_mode=False, force=False):
    """
    Delete a user from management authorization role
    """
    user_found = False
    ret_obj = ibmsecurity.isam.base.management_authorization.role.get(isamAppliance, name)

    if (ret_obj['data']['users'] != None):
        for usr in ret_obj['data']['users']:
            if usr['name'] == user_name:
                user_found = True
                ret_obj['data']['users'].remove(usr)
                break

    if user_found is False and force is False:
        return isamAppliance.create_return_object()

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Delete user from management authorization role",
            "/authorization/roles/{0}/v1".format(name), ret_obj['data'])
