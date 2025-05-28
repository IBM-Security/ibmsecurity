import logging

import ibmsecurity.isam.web.reverse_proxy.oauth2_configuration
import ibmsecurity.isam.appliance

import pytest

def getTestData():
    testdata = [
            {
                "hostname": "127.0.0.1",
                "port": "443",
                "reuse_certs": True,
                "load_certificate": True,
                "reuse_acls": True,
                "junction": "/isvaop"
            },
        ]
    return testdata


@pytest.mark.parametrize("items", getTestData())
def test_set_reverseproxy_isamop(iviaServer, caplog, items) -> None:
    """Set some isvaop stuff."""
    caplog.set_level(logging.DEBUG)

    arg = {}
    instance_id = 'default'
    for k, v in items.items():
        if k == 'instance_id':
            instance_id = v
            continue
        arg[k] = v

    returnValue = ibmsecurity.isam.web.reverse_proxy.oauth2_configuration.config(iviaServer,
                                                  instance_id,
                                                  force=False,
                                                  **arg)
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
