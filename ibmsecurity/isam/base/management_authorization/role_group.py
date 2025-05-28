import logging
import ibmsecurity.isam.base.management_authorization.role

logger = logging.getLogger(__name__)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieving the list of groups for an authorization roles
    """
    return isamAppliance.invoke_get("Retrieving the list of groups for an authorization roles",
                                    f"/authorization/roles/{name}/groups/v1")


def set(isamAppliance, name, group_name, type='embedded_ldap', check_mode=False, force=False):
    """
    Add a group to management authorization role
    """
    new_group = True
    ret_obj = ibmsecurity.isam.base.management_authorization.role.get(isamAppliance, name)

    if (ret_obj['data']['groups'] == None):
        ret_obj['data']['groups'] = []
    else:
        for grp in ret_obj['data']['groups']:
            if grp['name'] == group_name:
                if grp['type'] == type:
                    if force is False:
                        return isamAppliance.create_return_object()
                    new_group = False
                else:  # Replace group with new type
                    ret_obj['data']['groups'].remove(grp)
                break

    if new_group is True:
        ret_obj['data']['groups'].append({'name': group_name, 'type': type})

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Add group to management authorization role",
            f"/authorization/roles/{name}/v1", ret_obj['data'])


def delete(isamAppliance, name, group_name, check_mode=False, force=False):
    """
    Delete a group from management authorization role
    """
    group_found = False
    ret_obj = ibmsecurity.isam.base.management_authorization.role.get(isamAppliance, name)

    if (ret_obj['data']['groups'] != None):
        for grp in ret_obj['data']['groups']:
            if grp['name'] == group_name:
                group_found = True
                ret_obj['data']['groups'].remove(grp)
                break

    if group_found is False and force is False:
        return isamAppliance.create_return_object()

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Delete group from management authorization role",
            f"/authorization/roles/{name}/v1", ret_obj['data'])
