import logging

import ibmsecurity.isam.base.application_locale
import ibmsecurity.isam.appliance

import pytest

def getTestData():
    testdata = [
        {"id": "en_US.utf8"}

    ]
    return testdata


def test_get_log_language(iviaServer, caplog) -> None:
    """Get sms protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.application_locale.get(iviaServer,
                                                                **arg
                                                               )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestData())
def test_set_locale(iviaServer, caplog, items) -> None:
    """Set admin ssh keys"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}

    for k, v in items.items():
        #if k == 'id':
        #    id = v
        #    continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v

    returnValue = ibmsecurity.isam.base.application_locale.set(iviaServer, **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
