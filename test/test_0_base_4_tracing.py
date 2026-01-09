import logging
import pytest

import ibmsecurity.isam.base.tracing
import ibmsecurity.isam.appliance


def test_get_tracing(iviaServer, caplog) -> None:
    """Get tracing protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.tracing.get(iviaServer,
                                                     full_list=True,
                                                     deployed_policy=True
                                                    )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
