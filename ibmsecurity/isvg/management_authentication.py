import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isvgAppliance, check_mode=False, force=False):
    """
    Get management authentication
    """
    return isvgAppliance.invoke_get("Get management authentication",
                                    "/lmi_auth/")


def set(isvgAppliance,
        ldap_host=None,
        ldap_port=None,
        base_dn=None,
        admin_group_dn=None,
        enable_ssl=False,
        user_attribute='uid',
        group_member_attribute='member',
        bind_dn=None,
        bind_password=None,
        check_mode=False,
        force=False):
    """
    Set management authentication to remote
    """
    warnings = []
    update_required = False
    json_data = {
    }
    if ldap_host is not None:
        json_data['ldap_host'] = ldap_host
    if ldap_port is not None:
        json_data['ldap_port'] = ldap_port
    if enable_ssl is not None:
        json_data['enable_ssl'] = enable_ssl
    if user_attribute is not None:
        json_data['user_attribute'] = user_attribute
    if group_member_attribute is not None:
        json_data['group_member_attribute'] = group_member_attribute
    if base_dn is not None:
        json_data['base_dn'] = base_dn
    if admin_group_dn is not None:
        json_data['admin_group_dn'] = admin_group_dn
    if bind_dn is not None:
        json_data['bind_dn'] = bind_dn
    if bind_password is not None:
        json_data['bind_password'] = bind_password
    if force is False:
        if bind_password is not None:
            warnings.append("Unable to read existing bind password to check idempotency.")
            update_required = True
        else:
            ret_obj = get(isvgAppliance)
            if 'bind_dn' in ret_obj['data']:
                if ret_obj['data']['bind_dn'] is None:
                    del ret_obj['data']['bind_dn']
            sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
            logger.debug("Sorted input: {0}".format(sorted_json_data))
            sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
            logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
            if sorted_ret_obj != sorted_json_data:
                logger.info("Changes detected, update needed.")
                update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isvgAppliance.invoke_put(
                "Set management authentication to remote",
                "/lmi_auth/",
                json_data, warnings=warnings)

    return isvgAppliance.create_return_object()


def disable(isvgAppliance, check_mode=False, force=False):
    """
    Disable remote management authentication
    """
    return set(isvgAppliance=isvgAppliance, ldap_host=None, ldap_port=None, base_dn=None, admin_group_dn=None,
               enable_ssl=None, user_attribute=None,
               group_member_attribute=None, bind_dn=None, bind_password=None, check_mode=check_mode,
               force=force)


def test(isvgAppliance, userid, password, check_mode=False, force=False):
    """
    Testing the management authentication
    """
    ret_obj = isvgAppliance.invoke_post("Testing the management authentication",
                                        "/lmi_auth/",
                                           {
                                            'user': userid,
                                            'password': password
                                           }
                                       )
    ret_obj['changed'] = False

    return ret_obj


def compare(isvgAppliance1, isvgAppliance2):
    """
    Compare management authentication settings
    """
    ret_obj1 = get(isvgAppliance1)
    ret_obj2 = get(isvgAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
