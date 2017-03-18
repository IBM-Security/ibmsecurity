import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get management authentication
    """
    return isamAppliance.invoke_get("Get management authentication",
                                    "/isam/management_authentication/")


def set(isamAppliance,
        ldap_host,
        ldap_port,
        base_dn,
        admin_group_dn,
        enable_ssl=False,
        key_database=None,
        cert_label=None,
        user_attribute='uid',
        group_member_attribute='member',
        anon_bind=True,
        bind_dn=None,
        bind_password=None,
        check_mode=False,
        force=False):
    """
    Set management authentication to remote
    """
    if force is True or _check(isamAppliance) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Set management authentication to remote",
                "/isam/management_authentication/",
                {
                    'type': 'remote',
                    "ldap_host": ldap_host,
                    "ldap_port": ldap_port,
                    "enable_ssl": enable_ssl,
                    "key_database": key_database,
                    "cert_label": cert_label,
                    "user_attribute": user_attribute,
                    "group_member_attribute": group_member_attribute,
                    "base_dn": base_dn,
                    "admin_group_dn": admin_group_dn,
                    "anon_bind": anon_bind,
                    "bind_dn": bind_dn,
                    "bind_password": bind_password
                })

    return isamAppliance.create_return_object()


def _check(isamAppliance):
    """
    Check if management authentication set to remote
    """
    ret_obj = get(isamAppliance)

    if ret_obj['data']['type'] == 'local':
        return False
    else:
        return True


def disable(isamAppliance, check_mode=False, force=False):
    """
    Disable remote management authentication
    """
    if force is True or _check(isamAppliance) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Set management authentication to local",
                "/isam/management_authentication/",
                {
                    'type': 'local'
                })

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare management authentication settings
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
