import logging

import ibmsecurity.isam.base.audit.configuration
import ibmsecurity.isam.appliance

import pytest


def getTestData():
    testdata = [
        {
            "id": "1"
        }
    ]
    return testdata


def getTestDataAudit():
    testdata = [
        {
            "enabled": False,
            "id": "1",
            "type": "Syslog",
            "useJSONFormat": False,
            "verbose": False,
            "config": [
                {
                    "datatype": "Integer",
                    "key": "ISAM.Audit.syslogclient.MAX_QUEUE_SIZE",
                    "sensitive": False,
                    "validValues": [],
                    "value": "1000"
                },
                {
                    "datatype": "Integer",
                    "key": "ISAM.Audit.syslogclient.QUEUE_FULL_TIMEOUT",
                    "sensitive": False,
                    "validValues": [],
                    "value": "-1"
                },
                {
                    "datatype": "String",
                    "key": "ISAM.Audit.syslogclient.TRANSPORT",
                    "sensitive": False,
                    "validValues": [],
                    "value": "TRANSPORT_UDP"
                },
                {
                    "datatype": "Hostname",
                    "key": "ISAM.Audit.syslogclient.SERVER_HOST",
                    "sensitive": False,
                    "validValues": [],
                    "value": "127.0.0.1"
                },
                {
                    "datatype": "Integer",
                    "key": "ISAM.Audit.syslogclient.SERVER_PORT",
                    "sensitive": False,
                    "validValues": [],
                    "value": "514"
                },
                {
                    "datatype": "Boolean",
                    "key": "ISAM.Audit.syslogclient.CLIENT_CERT_AUTH_REQUIRED",
                    "sensitive": False,
                    "validValues": [],
                    "value": "false"
                },
                {
                    "datatype": "Integer",
                    "key": "ISAM.Audit.syslogclient.NUM_SENDER_THREADS",
                    "sensitive": False,
                    "validValues": [],
                    "value": "1"
                },
                {
                    "datatype": "Integer",
                    "key": "ISAM.Audit.syslogclient.NUM_RETRY",
                    "sensitive": False,
                    "validValues": [],
                    "value": "2"
                },
                {
                    "datatype": "Boolean",
                    "key": "ISAM.Audit.syslogclient.FAILOVER_TO_DISK",
                    "sensitive": False,
                    "validValues": [],
                    "value": "false"
                },
                {
                    "datatype": "String",
                    "key": "ISAM.Audit.syslogclient.CLIENT_AUTH_KEY",
                    "sensitive": False,
                    "validValues": [],
                    "value": "_"
                },
                {
                    "datatype": "String",
                    "key": "ISAM.Audit.syslogclient.SSL_TRUST_STORE",
                    "sensitive": False,
                    "validValues": [],
                    "value": ""
                },
                {
                    "datatype": "String",
                    "key": "ISAM.Audit.syslogclient.TAG",
                    "sensitive": False,
                    "validValues": [],
                    "value": "tag"
                }
            ],
        }]
    return testdata

def test_current_audit_configuration(iviaServer, caplog) -> None:
    """Get sms protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.audit.configuration.get(iviaServer,
                                                                **arg
                                                               )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestData())
def test_get_specific_audit_configuration(iviaServer, caplog, items) -> None:
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

    returnValue = ibmsecurity.isam.base.audit.configuration.get(iviaServer, **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestDataAudit())
def test_set_audit_configuration(iviaServer, caplog, items) -> None:
    """Set admin ssh keys"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    id, config = None, None
    for k, v in items.items():
        if k == 'id':
            id = v
            continue
        if k == 'config':
            config = v
            continue
        arg[k] = v

    returnValue = ibmsecurity.isam.base.audit.configuration.set(iviaServer, id, config, **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
