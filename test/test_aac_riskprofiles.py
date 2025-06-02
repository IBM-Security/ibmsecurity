import logging

import ibmsecurity.isam.aac.risk_profiles
import ibmsecurity.isam.appliance

import pytest

def getTestData():
    testdata = [
        {
            "name": "Risk profile 1",
            "active": True,
            "description": "Test for risk profiles",
            "attributes": [{"name": "accessTime", "weight": 60},
                           {"name": "http:userAgent", "weight": 10}]
        },
    ]
    return testdata


@pytest.mark.parametrize("items", getTestData())
def test_set_riskprofiles(iviaServer, caplog, items) -> None:
    """Set api protection"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    active = False
    for k, v in items.items():
        if k == 'name':
            name = v
            continue
        if k == 'active':
            active = v
            continue
        arg[k] = v

    returnValue = ibmsecurity.isam.aac.risk_profiles.set(iviaServer,
                                                                      name,
                                                                      active,
                                                                      **arg
                                                                      )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
