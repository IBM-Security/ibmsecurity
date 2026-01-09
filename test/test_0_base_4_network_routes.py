import logging
import os
import pytest

import ibmsecurity.isam.base.network.static_routes
import ibmsecurity.isam.appliance


def getTestData():
    testdata = [
        {
            "address": "default",
            "enabled": True,
            "gateway": f"{os.getenv('IVIA_HOST').split('.')[:-1]}.1",
            "metric": 100,
            "comment": "Default gateway set in test"
        },
    ]
    return testdata

# def set(isamAppliance, address, new_address=None, enabled=True, maskOrPrefix=None, gateway=None, metric=None,
#        comment=None, table='main', label=None, vlanId=None, new_label=None, new_vlanId=None, check_mode=False,
#        force=False):


@pytest.mark.parametrize("items", getTestData())
def test_set_default_route(iviaServer, caplog, items) -> None:
    """ibmsecurity/isam/base/network/static_routes.py"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    address = None
    for k, v in items.items():
        if k == 'address':
            address = v
            continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v

    returnValue = ibmsecurity.isam.base.network.static_routes.set(iviaServer,
                                                                  address,
                                                                  **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
