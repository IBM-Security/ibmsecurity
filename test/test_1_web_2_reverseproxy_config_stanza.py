import logging

import ibmsecurity.isam.web.reverse_proxy.configuration.stanza
import ibmsecurity.isam.web.reverse_proxy.instance
import ibmsecurity.isam.appliance

import pytest


def getTestData():
    testdata = [
        {
            "inst_name": "default",
            "stanza_id": "custom"
        },
        {
            "inst_name": "default",
            "stanza_id": "jwt:/"
        },
        {
            "inst_name": "test",
            "stanza_id": "custom"
        }
    ]
    return testdata


@pytest.mark.order(after="test_1_web_1_reverseproxy_setup.py::test_create_webseal_instance")
@pytest.mark.parametrize("items", getTestData())
def test_set_stanza(iviaServer, caplog, items) -> None:
    """ibmsecurity/isam/web/reverse_proxy/configuration/stanza.py"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    inst_name, stanza_id = None, None
    for k, v in items.items():
        if k == 'inst_name':
             inst_name = v
             continue
        if k == 'stanza_id':
             stanza_id = v
             continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v

    returnValue = ibmsecurity.isam.web.reverse_proxy.configuration.stanza.set(iviaServer, inst_name, stanza_id, **arg)
    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestData())
def test_delete_stanza(iviaServer, caplog, items) -> None:
    """ibmsecurity/isam/web/reverse_proxy/configuration/stanza.py"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    inst_name, stanza_id = None, None
    for k, v in items.items():
        if k == 'inst_name':
             inst_name = v
             continue
        if k == 'stanza_id':
             stanza_id = v
             continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v

    returnValue = ibmsecurity.isam.web.reverse_proxy.configuration.stanza.delete(iviaServer, inst_name, stanza_id, **arg)
    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()


def test_reverseproxy_commit_before_restart(iviaServer, caplog) -> None:
    caplog.set_level(logging.DEBUG)
    returnValue = ibmsecurity.isam.appliance.commit(iviaServer, publish=True)
    if returnValue is not None:
        assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestData())
def test_reverseproxy_restart_stanza(iviaServer, caplog, items) -> None:
    caplog.set_level(logging.DEBUG)
    arg = {}
    inst_name = None
    for k, v in items.items():
        if k == 'inst_name':
             inst_name = v
             continue
        if k == 'stanza_id':
             stanza_id = v
             continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v
    returnValue = ibmsecurity.isam.web.reverse_proxy.instance.execute(iviaServer, id=inst_name)
    if returnValue is not None:
        assert not returnValue.failed()
