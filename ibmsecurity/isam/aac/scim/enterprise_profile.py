import logging
import ibmsecurity.isam.aac.server_connections.ws
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"

def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current enterprise user profile SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current enterprise user profile SCIM configuration settings",
                                    "{0}/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)

def set(isamAppliance, mappings, check_mode=False, force=False):
    """
    Updating the enterprise user profile SCIM configuration settings

    """

    ret_obj = get(isamAppliance)
    old_obj = ret_obj['data']['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User']['mappings']
    new_obj = mappings['mappings']

    old_obj = json_sort(old_obj)
    new_obj = json_sort(new_obj)

    update_required = False
    found = False

    if len(old_obj) >= 1:
        if len(new_obj) >= 1:
            for obj in new_obj:
                for maping in ret_obj:
                    if obj == maping:
                        found = True
                if found is False:
                    update_required = True
        else:
            update_required = True
    else:
        if len(new_obj) >= 1:
            update_required = True


    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating the enterprise user profile SCIM configuration settings",
                                    "{0}/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User".format(uri),
                                    mappings,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )

    return isamAppliance.create_return_object(changed=False)