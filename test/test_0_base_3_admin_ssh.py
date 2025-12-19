import logging

import ibmsecurity.isam.base.admin_ssh_keys
import ibmsecurity.isam.appliance

import pytest

def getTestData():
    testdata = [
        {
            "name": "workstation",
            "key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILNvMjSUx0YEPNw0eAsHUERYl244CQfVWqCOTfo4joCe workstation"
        },
        {
            "name": "testuser",
            "key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILNvMjSUx0YEPNw0eAsHUERYl244CQfVWqCOTfo4joCe workstation",
            "fingerprint": "256 SHA256:kbJ4H0/nm7O5GdPNkXsNrG+oTlcaARU6ro64h3Y5WMY workstation (ED25519)"
        }
    ]
    return testdata


def test_get_admin_sshkeys(iviaServer, caplog) -> None:
    """Get sms protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.admin_ssh_keys.get_all(iviaServer,
                                                                **arg
                                                               )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestData())
def test_set_admin_sshkeys(iviaServer, caplog, items) -> None:
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

    returnValue = ibmsecurity.isam.base.admin_ssh_keys.set(iviaServer, **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
