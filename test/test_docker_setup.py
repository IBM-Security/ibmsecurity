# build stuff
import pytest

import logging

import ibmsecurity.isam.docker.base.network.db_configuration.configuration
import ibmsecurity.isam.appliance


def getTestData():
    testdata = [
        {
            "hvdb_db_type": "oracle",
            "hvdb_address": "oracledb",
            "hvdb_port": "1521",
            "hvdb_user": "dbadmin",
            "hvdb_password": "Passw0rd",
            "hvdb_db_name": "hvdb",
            "hvdb_driver_type": "thin",
            "hvdb_db_secure": True,
            "hvdb_db_truststore": "embedded_ldap_keys",
            "ignore_password_for_idempotency": True,
            "cfgdb_embedded": True
        },
        {
            "hvdb_db_type": "postgresql",
            "hvdb_address": "postgresql",
            "hvdb_port": "5432",
            "hvdb_user": "postgres",
            "hvdb_password": "Passw0rd",
            "hvdb_db_name": "ivia",
            "hvdb_db_secure": False,
            "ignore_password_for_idempotency": True,
            "cfgdb_embedded": True
        },
    ]
    return testdata

@pytest.mark.skipIf(iviaServer['facts']['model'] != "Docker")
@pytest.mark.order(after="test_base_firststeps.py::test_setup_complete")
def test_get_docker_dbconfig(iviaServer, caplog) -> None:
    """Get current config."""
    caplog.set_level(logging.DEBUG)

    returnValue = ibmsecurity.isam.docker.base.network.db_configuration.configuration.get(isamAppliance=iviaServer)
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()

@pytest.mark.order(after="test_base_firststeps.py::test_setup_complete")
@pytest.mark.parametrize("items", getTestData())
def test_set_docker_dbconfig(iviaServer, caplog, items) -> None:
    """Configure"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    for k, v in items.items():
        if k == 'hvdb_db_type':
            hvdb_db_type = v
            continue
        if k == 'hvdb_address':
            hvdb_address = v
            continue
        if k == 'hvdb_port':
            hvdb_port = v
            continue
        if k == 'hvdb_user':
            hvdb_user = v
            continue
        if k == 'hvdb_password':
            hvdb_password = v
            continue
        arg[k] = v

    returnValue = ibmsecurity.isam.docker.base.network.db_configuration.configuration.set(iviaServer,
                                                                                          hvdb_db_type,
                                                                                          hvdb_address,
                                                                                          hvdb_port,
                                                                                          hvdb_user,
                                                                                          hvdb_password,
                                                                                          **arg
                                                                                          )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
