import logging
import pytest

import ibmsecurity.isam.web.user_count
import ibmsecurity.isam.appliance

# @pytest.mark.order(after="test_get_base_admin")
def test_get_user_count(iviaServer, caplog) -> None:
    """Get user count (new in 11.0.2"""
    caplog.set_level(logging.DEBUG)

    returnValue = ibmsecurity.isam.web.user_count.get(isamAppliance=iviaServer)
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
