import logging
import ibmsecurity.isam.aac.server_connections.ws
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"

def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve configuration of SCIM ISAM user settings
    """
    return isamAppliance.invoke_get("Retrieve configuration of SCIM ISAM user settings",
                                    "{0}/urn:ietf:params:scim:schemas:extension:isam:1.0:User".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)

def set(isamAppliance, ldap_connection=None, isam_domain=None, update_native_users=None, connection_type=None, attrs_dir=None, enforce_password_policy=None, check_mode=False, force=False):
    """
    Updating the ISAM user SCIM configuration settings
    """
    ret_obj = get(isamAppliance)
    ret_obj = ret_obj['data']['urn:ietf:params:scim:schemas:extension:isam:1.0:User']

    new_obj = {}

    update_required = False

    if ldap_connection is None:
        if 'ldap_connection' in ret_obj:
            new_obj['ldap_connection'] = ret_obj['ldap_connection']
    else:
        new_obj['ldap_connection'] = ldap_connection
        if 'ldap_connection' in ret_obj:
            if ret_obj['ldap_connection'] != ldap_connection:
                update_required = True
        else:
            update_required = True

    if isam_domain is None:
        if 'isam_domain' in ret_obj:
            new_obj['isam_domain'] = ret_obj['isam_domain']
    else:
        new_obj['isam_domain'] = isam_domain
        if 'isam_domain' in ret_obj:
            if ret_obj['isam_domain'] != isam_domain:
                update_required = True
        else:
            update_required = True

    if update_native_users is None:
        if 'update_native_users' in ret_obj:
            new_obj['update_native_users'] = ret_obj['update_native_users']
    else:
        new_obj['update_native_users'] = update_native_users
        if 'update_native_users' in ret_obj:
            if ret_obj['update_native_users'] != update_native_users:
                update_required = True
        else:
            update_required = True

    if connection_type is None:
        if 'connection_type' in ret_obj:
            new_obj['connection_type'] = ret_obj['connection_type']
    else:
        new_obj['connection_type'] = connection_type
        if 'connection_type' in ret_obj:
            if ret_obj['connection_type'] != connection_type:
                update_required = True
        else:
            update_required = True

    if attrs_dir is None:
        if 'attrs_dir' in ret_obj:
            new_obj['attrs_dir'] = ret_obj['attrs_dir']
    else:
        new_obj['attrs_dir'] = attrs_dir
        if 'attrs_dir' in ret_obj:
            if ret_obj['attrs_dir'] != attrs_dir:
                update_required = True
        else:
            update_required = True

    if enforce_password_policy is None:
        if 'enforce_password_policy' in ret_obj:
            new_obj['enforce_password_policy'] = ret_obj['enforce_password_policy']
    else:
        new_obj['enforce_password_policy'] = enforce_password_policy
        if 'enforce_password_policy' in ret_obj:
            if ret_obj['enforce_password_policy'] != enforce_password_policy:
                update_required = True
        else:
            update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating the ISAM user SCIM configuration settings",
                "/mga/scim/configuration/urn:ietf:params:scim:schemas:extension:isam:1.0:User",
                new_obj, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(changed=False)