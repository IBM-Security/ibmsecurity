import logging
import os

import ibmsecurity.isam.web.runtime.process
import ibmsecurity.isam.appliance

import pytest


def getTestData():
    testdata = [
        {
                "admin_pwd": os.getenv('IVIA_SECMASTER_PW'),
                "ps_mode": "local",
                "user_registry": "local",
                "ldap_pwd": "passw0rd",
                "clean_ldap": "true",
                "admin_cert_lifetime": 1460,
                "ssl_compliance": "none"

        }
    ]
    return testdata

@pytest.mark.order(after="test_0_base_2_ssl_personalcerts.py::test_import_personal_cert")
@pytest.mark.parametrize("items", getTestData())
def test_configure_policy_runtime(iviaServer, caplog, items) -> None:
    """ibmsecurity/isam/web/runtime/process.py"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    for k, v in items.items():
        if k == 'admin_pwd':
             admin_pwd = v
             continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v

    returnValue = ibmsecurity.isam.web.runtime.process.config(iviaServer, admin_pwd, **arg)
    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
