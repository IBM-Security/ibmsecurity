import logging
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"

def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current user profile SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current user profile SCIM configuration settings",
                                    "/mga/scim/configuration/urn:ietf:params:scim:schemas:core:2.0:User",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def set(isamAppliance, ldap_connection, search_suffix, user_suffix, ldap_object_classes, mappings, user_dn=None, connection_type=None, attrs_dir=None, enforce_password_policy=None, check_mode=False, force=False):
    """
    Updating the user profile SCIM configuration settings
    """
    ret_obj = get(isamAppliance)
    ret_obj = ret_obj['data']['urn:ietf:params:scim:schemas:core:2.0:User']

    new_obj = {'ldap_connection': ldap_connection,
               'user_suffix': user_suffix,
               'search_suffix': search_suffix,
               'ldap_object_classes': ldap_object_classes,
               'mappings': mappings,
               }


    if user_dn is not None:
        new_obj['user_dn'] = user_dn
    else:
        new_obj['user_dn'] = ret_obj['user_dn']

    if connection_type is not None:
        new_obj['connection_type'] = connection_type
    else:
        new_obj['connection_type'] = ret_obj['connection_type']

    if attrs_dir is not None:
        new_obj['attrs_dir'] = attrs_dir
    else:
        new_obj['attrs_dir'] = ret_obj['attrs_dir']

    if enforce_password_policy is not None:
        new_obj['enforce_password_policy'] = enforce_password_policy
    else:
        new_obj['enforce_password_policy'] = ret_obj['enforce_password_policy']

    obj1 = json_sort(ret_obj)
    obj2 = json_sort(new_obj)

    update_required = False
    if obj1 != obj2:
        update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating the user profile SCIM configuration settings",
                "{0}/urn:ietf:params:scim:schemas:core:2.0:User".format(uri),
                new_obj, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()
