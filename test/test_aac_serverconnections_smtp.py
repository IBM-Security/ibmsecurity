import logging

import ibmsecurity.isam.aac.server_connections
import ibmsecurity.isam.aac.server_connections.smtp
import ibmsecurity.isam.appliance

import pytest

def getTestData():
    testdata = [
        {
            "connection": {
                "hostName": "smtp.isam-test.ibm.com",
                "hostPort": 587,
                "user": "isamUser",
                "password": "password",
                "ssl": False
            },
            "connectionManager": {
                "connectTimeout": 30
            },
            "name": "SMTPTestConnection",
            "description": "A test connection to a SMTP server",
            "locked": False
        }
    ]
    return testdata


def test_get_serverconnection_smtp(iviaServer, caplog) -> None:
    """Get sms protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.aac.server_connections.smtp.get_all(iviaServer,
                                                                      **arg
                                                                      )
    logging.log(logging.INFO, returnValue)


    assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestData())
def test_set_serverconnection_smtp(iviaServer, caplog, items) -> None:
    """Set api protection"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    connection = {}
    for k, v in items.items():
        if k == 'name':
            name = v
            continue
        if k == 'connection':
            connection = v
            continue
        arg[k] = v

    returnValue = ibmsecurity.isam.aac.server_connections.smtp.set(iviaServer,
                                                                      name,
                                                                      connection,
                                                                      **arg
                                                                      )
    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
