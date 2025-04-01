"""PyTest fixtures for testing the project."""
from __future__ import annotations

import pytest

from ibmsecurity.appliance.isamappliance import ISAMAppliance
from ibmsecurity.user.applianceuser import ApplianceUser
# pylint: disable=wildcard-import,unused-wildcard-import


class IviaLogin:
    def __init__(self):
        # Create a user credential for ISAM appliance
        u = ApplianceUser(username="admin@local", password="admin")
        # Create an ISAM appliance with above credential
        self.isam_server = ISAMAppliance(hostname="192.168.1.11", user=u, lmi_port=443)


@pytest.fixture
def iviaServer():
    s = IviaLogin()
    return s.isam_server


# ibmsecurity
def pytest_runtest_setup(item):
    print("setting up function:", item.name)


# @pytest.fixture(autouse=True)
# def pytest_configure(config: Config) -> None:
#   """Register custom markers."""
#    print('configure')
