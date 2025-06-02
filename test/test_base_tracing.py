import logging

import ibmsecurity.isam.base.tracing
import ibmsecurity.isam.appliance

import pytest




def test_get_tracing(iviaServer, caplog) -> None:
    """Get sms protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.tracing.get(iviaServer,
                                                     full_list=True,
                                                     deployed_policy=True
                                                    )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
