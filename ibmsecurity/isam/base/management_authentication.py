import logging
import ibmsecurity.utilities.tools
import json

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get management authentication
    """
    return isamAppliance.invoke_get("Get management authentication",
                                    "/isam/management_authentication/")


def set(isamAppliance,
        check_mode=False,
        force=False,
        ignore_password_for_idempotency=False,
        type='remote',
        **kwargs,
       ):
    """
    Set management authentication to remote

    ldap_host=None,
    ldap_port=None,
    base_dn=None,
    admin_group_dn=None,
    enable_ssl=False,
    key_database=None,
    cert_label=None,
    user_attribute='uid',
    group_member_attribute='member',
    anon_bind=True,
    bind_dn=None,
    bind_password=None,
    ldap_debug=None,
    enable_usermapping=False,
    usermapping_script=None,
    enable_ssh_pubkey_auth
    ssh_pubkey_auth_attribute=None
    oidc_client_id	String	No	The OIDC Client Identifier. This field is required if type == "federation".
    oidc_client_secret	String	No	The OIDC Client Secret. This field is required if type == "federation".
    oidc_discovery_endpoint	String	No	The OIDC Discovery (well-known) endpoint. This field is required if type == "federation".
    oidc_enable_pkce	Boolean	No	Specifies whether the Public key Code Exchange extension is enforced. This field is required if type == "federation".
    oidc_enable_admin_group	Boolean	No	Specifies whether a user must be a member of a particular group to be considered an administrator user. This field is required if type == "federation".
    oidc_group_claim	String	Yes	The OIDC token claim to use as group membership. This claim can either be a String, or a list of Strings. The default value is "groups".
    oidc_admin_group	String	Yes	The name of the group which a user must be a member of to be considered an administrator user. The default value is "adminGroup".
    oidc_user_claim	String	Yes	Specifies the OIDC token claim to use as the username. The default value is "sub".
    oidc_keystore	String	Yes	The SSL Truststore to verify connections the the OIDC OP. The default value if "lmi_trust_store".
    enable_tokenmapping	Boolean	No	Specifies whether custom claim to identity mapping is performed using a JavaScript code fragment. This field is required if type == "federation".
    tokenmapping_script	String	Yes	The custom JavaScript code fragment to map an identity token to a username/group membership.

    """
    warnings = []
    update_required = False

    json_data = {
        'type': type
    }
    for k, v in kwargs.items():
        if k  == 'ldap_debug' and v == '':
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "9.0.4.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, ldap_debug: {ldap_debug} is not supported. Needs 9.0.4.0 or higher. Ignoring ldap_debug for this call.")
                continue
        if k == 'enable_usermapping':
            # only valid if type == remote
            if type == 'remote':
                if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.2.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, {k}: {v} is not supported. Needs 10.0.2.0 or higher. Ignoring {k} for this call.")
                    continue
            else:
                warnings.append(f"{k} is only supported for type remote. Ignoring it for now.")
                continue
        if k in ('ssh_pubkey_auth_attribute','enable_ssh_pubkey_auth'):
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.6") < 0:
                warnings.append(f"Appliance at version: {isamAppliance.facts['version']}, {k}: {v} is not supported. Needs 10.0.8.0 or higher. Ignoring {k} for this call.")
                continue
        if k.startswith('oidc_') or k in ('enable_tokenmapping', 'tokenmapping_script'):
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.8") < 0:
                warnings.append(f"Appliance at version: {isamAppliance.facts['version']}, {k}: {v} is not supported. Needs 10.0.8.0 or higher. Ignoring {k} for this call.")
                continue
        json_data[k] = v
    # Set defaults for type remote and cleanup
    if type == 'remote':
        if json_data.get('user_attribute', None) is None:
            json_data['user_attribute'] = 'uid'
        if json_data.get('group_member_attribute', None) is None:
            json_data['group_member_attribute'] = 'member'
        if json_data.get('anon_bind', None) is None:
            json_data['anon_bind'] = True
        if not json_data.get('enable_usermapping', False):
           json_data["usermapping_script"] = ''

    # Defaults for type federation (new in 10.0.8) and cleanup
    if type == 'federation':
        if json_data.get('oidc_group_claim', None) is None:
            json_data['oidc_group_claim'] = 'groups'
        if json_data.get('oidc_admin_group', None) is None:
            json_data['oidc_admin_group'] = 'adminGroup'
        if json_data.get('oidc_user_claim', None) is None:
            json_data['oidc_user_claim'] = "sub"
        if json_data.get('oidc_keystore', None) is None:
            json_data['oidc_keystore'] = "lmi_trust_store"
        if not json_data.get('enable_tokenmapping', False):
            json_data["tokenmapping_script"] = ''

    if not force:
        if not ignore_password_for_idempotency and json_data.get('bind_password', None) is not None:
            warnings.append("Unable to read existing bind password to check idempotency.  You can disable this behaviour by passing `ignore_password_for_idempotency=True`")
            update_required = True
        else:
            ret_obj = get(isamAppliance)
            json_data_compare = json_data.copy()
            if json_data.get("bind_dn", None) is None:
                ret_obj["data"].pop("bind_dn", None)
            ret_obj["data"].pop("bind_password", None)
            json_data_compare.pop("bind_password", None)
            sorted_json_data = json.dumps(json_data_compare, skipkeys=True, sort_keys=True)
            logger.debug(f"\n\nSorted input:         {sorted_json_data}")
            sorted_ret_obj = json.dumps(ret_obj['data'], skipkeys=True, sort_keys=True)
            logger.debug(f"\n\nSorted existing data: {sorted_ret_obj}")
            if sorted_ret_obj != sorted_json_data:
                logger.info("Changes detected, update needed.")
                update_required = True

    if force or update_required:
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                f"Set management authentication to {type}",
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
