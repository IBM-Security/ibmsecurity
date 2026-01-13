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
