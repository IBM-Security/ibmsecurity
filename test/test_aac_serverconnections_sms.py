import logging

import ibmsecurity.isam.aac.server_connections
import ibmsecurity.isam.aac.server_connections.sms
import ibmsecurity.isam.appliance

import pytest

def getTestData():
    testdata = [
        {
         "connection": {
           "url": "https://localhost",
           "user": "isamUser",
           "password": "password",
           "sslTruststore": "lmi_trust_store",
           "sslAuthKey": "server"
         },
         "connectionManager": {
           "requestParameters": "from = +12345678, to = $DEST_NO$, message = $MSG$",
           "successReturnCode": "201",
           "responseBodyRegex": ".*"
         },
         "name": "SMSTestConnection",
         "description": "A test connection to a SMS server",
         "locked": False,
         "ignore_password_for_idempotency": True
        }
    ]
    return testdata


def test_get_serverconnection_sms(iviaServer, caplog) -> None:
    """Get sms protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.aac.server_connections.sms.get_all(iviaServer,
                                                                      **arg
                                                                      )
    logging.log(logging.INFO, returnValue)


    assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestData())
def test_set_serverconnection_sms(iviaServer, caplog, items) -> None:
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

    returnValue = ibmsecurity.isam.aac.server_connections.sms.set(iviaServer,
                                                                      name,
                                                                      connection,
                                                                      **arg
                                                                      )
    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
