import logging

import ibmsecurity.isam.base.ssl_certificates.certificate_databases
import ibmsecurity.isam.appliance

import pytest

def getTestData():
    testdata = [
        {
            "kdb_name": "junctionkdb",
            "type": "kdb"
        },
        {
            "kdb_name": "ncipherdb",
            "type": "p11",
            "token_label": "label",
            "passcode": "passcode",
            "hsm_type": "ncipher",
            "ip": "10.150.25.207",
            "rfs": "10.150.25.208"
        }
    ]
    return testdata


def test_get_certificate_databases(iviaServer, caplog) -> None:
    """Get sms protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.ssl_certificates.certificate_databases.get_all(iviaServer,
                                                                **arg
                                                               )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestData())
def test_create_certificate_database(iviaServer, caplog, items) -> None:
    """Set admin ssh keys"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    kdb_name = None
    for k, v in items.items():
        if k == 'kdb_name':
            kdb_name = v
            continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v

    returnValue = ibmsecurity.isam.base.ssl_certificates.certificate_databases.create(iviaServer, kdb_name,
                                                                                      **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestData())
def test_update_certificate_database(iviaServer, caplog, items) -> None:
    """Set admin ssh keys"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    cert_id = None
    for k, v in items.items():
        if k == 'cert_id':
            cert_id = v
            continue
        if k == 'kdb_name':
            cert_id = v
            continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v

    returnValue = ibmsecurity.isam.base.ssl_certificates.certificate_databases.set(iviaServer, cert_id, **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
