"""PyTest fixtures for testing the project."""
from __future__ import annotations

import os

import pytest

from ibmsecurity.appliance.isamappliance import ISAMAppliance
from ibmsecurity.user.applianceuser import ApplianceUser
import ibmsecurity.isam.appliance

@pytest.fixture(scope="session")
def iviaServer():
    """Initiate an ISAMAppliance."""
    # s = IviaLogin()
    _username = os.getenv('IVIA_ADMIN')
    _pw = os.getenv('IVIA_PW')
    _host = os.getenv('IVIA_HOST')
    _port = os.getenv('IVIA_PORT') or 443
    # Create a user credential for ISAM appliance
    u = ApplianceUser(username=_username, password=_pw)
    # Create an ISAM appliance with above credential
    isam_server = ISAMAppliance(hostname=_host, user=u, lmi_port=_port)
    yield isam_server
    returnValue = ibmsecurity.isam.appliance.commit(isamAppliance=isam_server, publish=True)
    print('\nCommit result and publish')
    print( returnValue )
    print('\n')
    return returnValue

# ibmsecurity
def pytest_runtest_setup(item):
    print("setting up function:", item.name)
    yield


# @pytest.fixture(autouse=True)
# def pytest_configure(config: Config) -> None:
#   """Register custom markers."""
#    print('configure')

#@pytest.fixture(scope="session", autouse=True)
#def ivia_commit(iviaServer):
#   """Commit the changes"""
#   print('TEST')
#   # caplog.set_level(logging.INFO)

#   returnValue = ibmsecurity.isam.appliance.commit(isamAppliance=iviaServer)
#   # logging.log(logging.DEBUG, returnValue)
#   print(returnValue)

#@pytest.hookimpl(hookwrapper=True)
#def pytest_sessionfinish(session, iviaServer):
#   """Commit the changes"""
#   # caplog.set_level(logging.INFO)
#
#   returnValue = ibmsecurity.isam.appliance.commit(isamAppliance=iviaServer)
#   yield returnValue
#        # logging.log(logging.DEBUG, returnValue)
#   print(returnValue)
#   print("\nTest session finished!")
