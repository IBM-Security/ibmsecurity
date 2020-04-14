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
        ldap_host=None,
        ldap_port=None,
        base_dn=None,
        admin_group_dn=None,
        type='remote',
        enable_ssl=False,
        key_database=None,
        cert_label=None,
        user_attribute='uid',
        group_member_attribute='member',
        anon_bind=True,
        bind_dn=None,
        bind_password=None,
        ldap_debug=None,
        check_mode=False,
        force=False):
    """
    Set management authentication to remote
    """
    warnings = []
    update_required = False
    json_data = {
        'type': type
    }
    if ldap_host is not None:
        json_data["ldap_host"] = ldap_host
    if ldap_port is not None:
        json_data["ldap_port"] = ldap_port
    if enable_ssl is not None:
        json_data["enable_ssl"] = enable_ssl
    if key_database is not None:
        json_data["key_database"] = key_database
    if cert_label is not None:
        json_data["cert_label"] = cert_label
    if user_attribute is not None:
        json_data["user_attribute"] = user_attribute
    if group_member_attribute is not None:
        json_data["group_member_attribute"] = group_member_attribute
    if base_dn is not None:
        json_data["base_dn"] = base_dn
    if admin_group_dn is not None:
        json_data["admin_group_dn"] = admin_group_dn
    if anon_bind is not None:
        json_data["anon_bind"] = anon_bind
    if bind_dn is not None:
        json_data["bind_dn"] = bind_dn
    if bind_password is not None:
        json_data["bind_password"] = bind_password
    if ldap_debug is not None or ldap_debug == '':
        if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                "Appliance at version: {0}, ldap_debug: {1} is not supported. Needs 9.0.4.0 or higher. Ignoring ldap_debug for this call.".format(
                    isamAppliance.facts["version"], ldap_debug))
        else:
            json_data["ldap_debug"] = ldap_debug
    elif ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") >= 0:
        json_data["ldap_debug"] = False
    if force is False:
        if bind_password is not None:
            warnings.append("Unable to read existing bind password to check idempotency.")
            update_required = True
        else:
            ret_obj = get(isamAppliance)
            if "bind_dn" in ret_obj['data']:
                if ret_obj["data"]["bind_dn"] is None:
                    del ret_obj["data"]["bind_dn"]
            sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
            logger.debug("Sorted input: {0}".format(sorted_json_data))
            sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
            logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
            if sorted_ret_obj != sorted_json_data:
                logger.info("Changes detected, update needed.")
                update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Set management authentication to remote",
                "/isam/management_authentication/",
                json_data, warnings=warnings)

    return isamAppliance.create_return_object()


def disable(isamAppliance, check_mode=False, force=False):
    """
    Disable remote management authentication
    """
    return set(isamAppliance=isamAppliance, ldap_host=None, ldap_port=None, base_dn=None, admin_group_dn=None,
               type='local', enable_ssl=None, key_database=None, cert_label=None, user_attribute=None,
               group_member_attribute=None, anon_bind=None, bind_dn=None, bind_password=None, check_mode=check_mode,
               force=force)


def test(isamAppliance, userid, password, check_mode=False, force=False):
    """
    Testing the management authentication
    """
    ret_obj = isamAppliance.invoke_post("Testing the management authentication",
                                        "/isam/management_authentication/",
                                           {
                                            'user': userid,
                                            'password': password
                                           }
                                       )
    ret_obj['changed'] = False

    return ret_obj


def compare(isamAppliance1, isamAppliance2):
    """
    Compare management authentication settings
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
