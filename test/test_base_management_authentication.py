import logging

import ibmsecurity.isam.base.management_authentication
import ibmsecurity.isam.appliance

import pytest

def getTestData():
    testdata = [
            {
                "type": "remote",
                "ignore_password_for_idempotency": True,
                "ldap_host": "127.0.0.1",
                "ldap_port": 636,
                "enable_ssl": True,
                "key_database": "lmi_trust_store",
                "cert_label": "server",
                "user_attribute": "uid",
                "group_member_attribute": "groups",
                "base_dn": "base DN",
                "admin_group_dn": "adminGroup",
                "anon_bind": False,
                "bind_dn": "cn=root",
                "bind_password": "bind password",
                "ldap_debug": False,
                "enable_usermapping": False,
                "usermapping_script": "function mapUser(props){...}",
                "enable_ssh_pubkey_auth": True,
                "ssh_pubkey_auth_attribute": "sshKey"
            },
        ]
    return testdata

def getTestDataSSO():
    testdata = [
            {
                "type": "federation",
                "ignore_password_for_idempotency": False,
                "oidc_client_id": "clientId",
                "oidc_client_secret": "clientSecret",
                "oidc_discovery_endpoint": "https://www.myidp.ibm.com/mga/sps/oauth/oauth20/metadata/TEST",
                "oidc_enable_pkce": True,
                "enable_tokenmapping": True,
                "tokenmapping_script": "function mapToken(operation, token){return 0;}"
            },
        ]
    return testdata

@pytest.mark.parametrize("items", getTestData())
def test_set_base_management_authentication_remote(iviaServer, caplog, items) -> None:
    """Set some admincfg options."""
    caplog.set_level(logging.DEBUG)

    arg = {}
    type = 'remote'
    ignore_password_for_idempotency = False
    for k, v in items.items():
        if k == 'type':
            type = v
            continue
        if k == 'ignore_password_for_idempotency':
            ignore_password_for_idempotency = v
        arg[k] = v

    returnValue = ibmsecurity.isam.base.management_authentication.set(isamAppliance=iviaServer,
                                                  force=False,
                                                  type=type,
                                                  **arg)
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()

@pytest.mark.parametrize("items", getTestDataSSO())
def test_set_base_management_authentication_federation(iviaServer, caplog, items) -> None:
    """Set some admincfg options."""
    caplog.set_level(logging.DEBUG)

    arg = {}
    type = 'remote'
    ignore_password_for_idempotency = False
    for k, v in items.items():
        if k == 'type':
            type = v
            continue
        if k == 'ignore_password_for_idempotency':
            ignore_password_for_idempotency = v
        arg[k] = v

    returnValue = ibmsecurity.isam.base.management_authentication.set(isamAppliance=iviaServer,
                                                  force=False,
                                                  type=type,
                                                  **arg)
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
