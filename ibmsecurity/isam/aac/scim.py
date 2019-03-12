import logging

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the complete list of SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the complete list of SCIM configuration settings",
                                    "/mga/scim/configuration")


def get_user_profile(isamAppliance, check_mode=False, force=False):
    """
    Retrieve configuration of SCIM user profile settings
    """
    ret_obj = isamAppliance.invoke_get("Retrieve configuration of SCIM user profile settings",
                                       "/mga/scim/configuration/urn:ietf:params:scim:schemas:core:2.0:User")
    return ret_obj['data']['urn:ietf:params:scim:schemas:core:2.0:User']


def get_isam_user(isamAppliance, check_mode=False, force=False):
    """
    Retrieve configuration of SCIM ISAM user settings
    """
    ret_obj = isamAppliance.invoke_get("Retrieve configuration of SCIM ISAM user settings",
                                       "/mga/scim/configuration/urn:ietf:params:scim:schemas:extension:isam:1.0:User")
    return ret_obj['data']['urn:ietf:params:scim:schemas:extension:isam:1.0:User']


def update_user_profile(isamAppliance, ldap_connection, user_suffix, search_suffix, check_mode=False, force=False):
    """
    Update SCIM user profile settings
    """
    ret_obj = get_user_profile(isamAppliance)
    del ret_obj['ldap_connection']
    del ret_obj['user_suffix']
    del ret_obj['search_suffix']

    ret_obj['ldap_connection'] = ldap_connection
    ret_obj['user_suffix'] = user_suffix
    ret_obj['search_suffix'] = search_suffix
    return isamAppliance.invoke_put(
        "Update SCIM user profile settings",
        "/mga/scim/configuration/urn:ietf:params:scim:schemas:core:2.0:User",
        ret_obj)


def update_isam_user(isamAppliance, isam_domain, update_native_users, ldap_connection, check_mode=False, force=False):
    """
    Update SCIM ISAM user settings
    """
    ret_obj = get_isam_user(isamAppliance)
    del ret_obj['isam_domain']
    del ret_obj['update_native_users']
    del ret_obj['ldap_connection']

    ret_obj['isam_domain'] = isam_domain
    ret_obj['update_native_users'] = update_native_users
    ret_obj['ldap_connection'] = ldap_connection
    return isamAppliance.invoke_put(
        "Update SCIM ISAM user settings",
        "/mga/scim/configuration/urn:ietf:params:scim:schemas:extension:isam:1.0:User",
        ret_obj)
