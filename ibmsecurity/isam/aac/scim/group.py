import logging
import ibmsecurity.isam.aac.server_connections.ws
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current group SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current group SCIM configuration settings",
                                    "{0}/urn:ietf:params:scim:schemas:core:2.0:Group".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )

def set(isamAppliance, ldap_object_classes, group_dn, check_mode=False, force=False):
    """
    Updating the group SCIM configuration settings
    """
    obj = get(isamAppliance)
    obj = obj['data']['urn:ietf:params:scim:schemas:core:2.0:Group']

    current_dn = obj['group_dn']
    current_classes = obj['ldap_object_classes']

    if current_dn == group_dn:
        sorted_new = json_sort(ldap_object_classes)
        sorted_old = json_sort(current_classes)
        if sorted_new == sorted_old:
            update_required = False
        else:
            update_required = True
    else:
        update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            data = {}
            data['group_dn'] = group_dn
            data['ldap_object_classes'] = ldap_object_classes
            return isamAppliance.invoke_put("Updating the group SCIM configuration settings",
                                            "{0}/urn:ietf:params:scim:schemas:core:2.0:Group".format(uri),
                                            data,
                                            requires_modules=requires_modules,
                                            requires_version=requires_version
                                            )

    return isamAppliance.create_return_object(changed=False)