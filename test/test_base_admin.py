import logging


# from ibmsecurity.appliance.isamappliance import ISAMAppliance
# from ibmsecurity.user.applianceuser import ApplianceUser
import ibmsecurity
import ibmsecurity.isam.base.admin

# Share credentials from conftest
# from conftest import iviaLogin


def test_get_base_admin(iviaServer, caplog) -> None:
    caplog.set_level(logging.DEBUG)

    returnValue = ibmsecurity.isam.base.admin.get(isamAppliance=iviaServer)

    logging.log(logging.INFO, returnValue)
    assert not returnValue.failed()
