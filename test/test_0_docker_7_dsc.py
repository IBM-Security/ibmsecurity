import logging

import ibmsecurity.isam.base.dsc
import ibmsecurity.isam.appliance

import pytest


def getTestData():
    testdata = [
        {
            "worker_threads": 64,
            "max_session_lifetime": 3600,
            "client_grace": 600,
            "connection_idle_timeout": 10,
            "service_port": 443,
            "replication_port": 444,
            "servers": [
                {
                    "ip": "10.0.0.1",
                    "service_port": 6443,
                    "replication_port": 6444
                },
                {
                    "ip": "10.0.0.1",
                    "service_port": 7443,
                    "replication_port": 7444
                },
            ]
        }
            ]
    return testdata


@pytest.mark.parametrize("items", getTestData())
def test_set_dsc_configuration(iviaServer, caplog, items) -> None:
    """Set admin ssh keys"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    for k, v in items.items():
        #if k == 'name':
        #    name = v
        #    continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v

    returnValue = ibmsecurity.isam.base.dsc.set(iviaServer, **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
