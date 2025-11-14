import logging

import ibmsecurity.isam.base.ssl_certificates.personal_certificate
import ibmsecurity.isam.appliance
import pytest

import os

def getTestData():
    testdata = [
        {
            "kdb_id": "pdsrv",
            "label": "syslogng.tbosmans.ibm.com",
            "cert": "test/scripts/syslogng.p12",
            "password": os.getenv('IVIA_SSL_PASSWORD')
        }
    ]
    return testdata

def test_get_all_personal_certs(iviaServer, caplog) -> None:
    """Get all personal certs protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.ssl_certificates.personal_certificate.get_all(iviaServer,
                                                                                      "pdsrv",
                                                                                       **arg
                                                                      )
    logging.log(logging.INFO, returnValue)


    assert not returnValue.failed()

@pytest.mark.parametrize("items", getTestData())
def test_import_personal_cert(iviaServer, caplog, items) -> None:
    """Import personal certs"""
    caplog.set_level(logging.DEBUG)
    logging.log(logging.INFO, items)
    arg = {}
    kdb_id = None
    cert = None
    label = None
    for k, v in items.items():
        if k == 'kdb_id':
            kdb_id = v
            continue
        if k == 'cert':
            cert = v
            continue
        if k == 'label':
            label = v
            continue
        arg[k] = v
    returnValue = ibmsecurity.isam.base.ssl_certificates.personal_certificate.import_cert(iviaServer,
                                                                                        kdb_id,
                                                                                        cert,
                                                                                        label,
                                                                                        **arg
                                                                                        )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
