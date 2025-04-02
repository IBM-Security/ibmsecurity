"""PyTest fixtures for testing the project."""
from __future__ import annotations

import os

import pytest

from ibmsecurity.appliance.isamappliance import ISAMAppliance
from ibmsecurity.user.applianceuser import ApplianceUser


@pytest.fixture
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
    return isam_server


# ibmsecurity
def pytest_runtest_setup(item):
    print("setting up function:", item.name)


# @pytest.fixture(autouse=True)
# def pytest_configure(config: Config) -> None:
#   """Register custom markers."""
#    print('configure')
