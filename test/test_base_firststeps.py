import pytest

import logging
import ibmsecurity.isam.base.service_agreement
import ibmsecurity.isam.base.setup_complete
import ibmsecurity.isam.appliance


def getTestData():
    testdata = [
        {
            "id": "1"
        }
    ]
    return testdata

@pytest.mark.order(0)
def test_set_service_agreement(iviaServer, caplog) -> None:
    """Get sms protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.service_agreement.set(iviaServer,
                                                                **arg
                                                               )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()


# FIPS is missing

@pytest.mark.order(1)
def test_setup_complete(iviaServer, caplog) -> None:
    """Mark setup complete"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.setup_complete.set(iviaServer,
                                                                **arg
                                                               )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()

    if returnValue.get("changed", False):
        returnValue = ibmsecurity.isam.appliance.commit_and_restart(iviaServer)
        assert not returnValue.failed()
