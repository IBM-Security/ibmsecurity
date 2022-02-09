import logging
import ibmsecurity.isam.aac.server_connections.ws
from ibmsecurity.utilities.tools import json_sort
import json

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"



def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current general SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current general SCIM configuration settings",
                                    "{0}/general".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )

def set(isamAppliance, enable_header_authentication=None, enable_authz_filter=None, admin_group=None, max_user_responses=None, attribute_modes=None, check_mode=False, force=False):
    """
    Updating the general SCIM configuration settings
    """
    ret_obj = get(isamAppliance)
    ret_obj = ret_obj['data']


    new_obj = {}


    if enable_header_authentication is None:
        new_obj['enable_header_authentication'] = ret_obj['enable_header_authentication']
    else:
        new_obj['enable_header_authentication'] = enable_header_authentication

    if enable_authz_filter is None:
        new_obj['enable_authz_filter'] = ret_obj['enable_authz_filter']
    else:
        new_obj['enable_authz_filter'] = enable_authz_filter

    if admin_group is None:
        new_obj['admin_group'] = ret_obj['admin_group']
    else:
        new_obj['admin_group'] = admin_group

    if max_user_responses is not None:
        new_obj['max_user_responses'] = max_user_responses
    else:
        if 'max_user_responses' in ret_obj:
            new_obj['max_user_responses'] = ret_obj['max_user_responses']

    if attribute_modes is not None:
        new_obj['attribute_modes'] = attribute_modes
    else:
        if 'attribute_modes' in ret_obj:
            new_obj['attribute_modes'] = ret_obj['attribute_modes']

    obj1 = json_sort(ret_obj)
    obj2 = json_sort(new_obj)


    if obj1 == obj2:
        update_required = False
    else:
        update_required = True


    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating the ISAM user SCIM configuration settings",
                "{0}/general".format(uri),
                new_obj, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(changed=False)