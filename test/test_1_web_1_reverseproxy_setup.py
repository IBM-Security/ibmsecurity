import logging
import os

import ibmsecurity.isam.web.reverse_proxy.instance
import ibmsecurity.isam.appliance

import pytest


def getTestData():
    testdata = [
        {
            "inst_name": "default",
            "host": os.getenv('IVIA_HOST'),
            "listening_port": "7239",
            "admin_id": os.getenv('IVIA_SECMASTER'),
            "admin_pwd": os.getenv('IVIA_SECMASTER_PW'),
            "http_yn": "no",
            "http_port": 80,
            "https_yn": "yes",
            "https_port": 8444,
            "nw_interface_yn": "yes",
            "ip_address": "0.0.0.0"
        },
        {
            "inst_name": "test",
            "host": os.getenv('IVIA_HOST'),
            "listening_port": "7255",
            "admin_id": os.getenv('IVIA_SECMASTER'),
            "admin_pwd": os.getenv('IVIA_SECMASTER_PW'),
            "http_yn": "no",
            "http_port": 80,
            "https_yn": "yes",
            "https_port": 8445,
            "nw_interface_yn": "yes",
            "ip_address": "0.0.0.0"
        }
    ]
    return testdata

@pytest.mark.order(after="test_1_web_0_policyruntime.py::test_configure_policy_runtime")
@pytest.mark.parametrize("items", getTestData())
def test_create_webseal_instance(iviaServer, caplog, items) -> None:
    """ibmsecurity/isam/web/runtime/process.py"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    inst_name = None
    for k, v in items.items():
        if k == 'inst_name':
             inst_name = v
             continue
        if k == 'admin_pwd':
             admin_pwd = v
             continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v

    returnValue = ibmsecurity.isam.web.reverse_proxy.instance.add(iviaServer, inst_name, admin_pwd, **arg)
    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
