import logging
import ibmsecurity.isam.base.management_authorization.role

logger = logging.getLogger(__name__)


def set(isamAppliance, name, feature_name, access=None, check_mode=False, force=False):
    """
    Set feature with access in management authorization role
    """
    new_feature = True
    ret_obj = ibmsecurity.isam.base.management_authorization.role.get(isamAppliance, name)

    if (ret_obj['data']['features'] == None):
        ret_obj['data']['features'] = []
    else:
        for ftr in ret_obj['data']['features']:
            if ftr['name'] == feature_name:
                new_feature = False
                if ftr['access'] != access:
                    ftr['access'] = access
                elif force is False:  # Everything matches, if no force return
                    return isamAppliance.create_return_object()
                break

    if new_feature is True:
        ret_obj['data']['features'].append({'name': feature_name, 'access': access})

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Add group to management authorization role",
            f"/authorization/roles/{name}/v1", ret_obj['data'])


def delete(isamAppliance, name, feature_name, check_mode=False, force=False):
    """
    Delete a feature from management authorization role
    """
    feature_found = False
    ret_obj = ibmsecurity.isam.base.management_authorization.role.get(isamAppliance, name)

    if (ret_obj['data']['features'] != None):
        for ftr in ret_obj['data']['features']:
            if ftr['name'] == feature_name:
                feature_found = True
                ret_obj['data']['features'].remove(ftr)
                break

    if feature_found is False and force is False:
        return isamAppliance.create_return_object()

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Delete feature from management authorization role",
            f"/authorization/roles/{name}/v1", ret_obj['data'])
