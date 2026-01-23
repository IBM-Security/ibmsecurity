import logging

import ibmsecurity.isam.web.reverse_proxy.configuration.entry
import ibmsecurity.isam.appliance

import pytest


def getTestData():
    testdata = [
        {
            "inst_name": "default",
            "stanza_id": "ssl-qop-mgmt-default",
            "entries": [
                ["default", 'TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384'],
                ["default", 'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384'],
                ["default", 'TLS_RSA_WITH_AES_256_GCM_SHA384'],
                ["default", 'TLS_CHACHA20_POLY1305_SHA256'],
            ]
        },
        {
            "inst_name": "default",
            "stanza_id": "jwt:/",
            "entries": [
                ["key-label", "syslogng.tbosmans.ibm.com"],
                ["claims", "text::ibm.com::iss"],
                ["claims", "text::test::test"],
            ]
        },
        {
            "inst_name": "default",
            "stanza_id": "logging",
            "entries": [
                ["request-log-format", 'client=%h, ident=%l, user=%u, time=%t, request="%r", status=%s, size=%b, http_user_agent="%{User-Agent}i", response_time=%F, junction=%j, junction_status=%c, junction_server=%S, junction_response_time=%J, incoming_isva_session_cookie=%{PD-S-SESSION-ID}e, outgoing_isva_session_cookie=%{PD-S-SESSION-ID}E, REFERER="%{referer}i"'],
            ]
        },
    ]
    return testdata


@pytest.mark.order(after="test_1_web_1_reverseproxy_setup.py::test_create_webseal_instance")
@pytest.mark.parametrize("items", getTestData())
def test_set_stanza_entries(iviaServer, caplog, items) -> None:
    """ibmsecurity/isam/web/reverse_proxy/configuration/stanza.py"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    inst_name, reverseproxy_id, stanza_id, entries = None, None, None, None
    for k, v in items.items():
        if k == 'inst_name':
             inst_name = v
             continue
        if k == 'reverseproxy_id':
             inst_name = v
             continue
        if k == 'stanza_id':
             stanza_id = v
             continue
        if k == 'entries':
             entries = v
             continue
        #if k == 'key':
        #    key = v
        #    continue
        arg[k] = v

    returnValue = ibmsecurity.isam.web.reverse_proxy.configuration.entry.set(iviaServer, inst_name, stanza_id, entries, **arg)
    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()


#@pytest.mark.parametrize("items", getTestData())
#def test_delete_stanza(iviaServer, caplog, items) -> None:
#    """ibmsecurity/isam/web/reverse_proxy/configuration/stanza.py"""
#    caplog.set_level(logging.DEBUG)
#    # items is a key-value pair
#    logging.log(logging.INFO, items)
#    arg = {}
#    inst_name, stanza_id = None, None
#    for k, v in items.items():
#        if k == 'inst_name':
#             inst_name = v
#             continue
#        if k == 'stanza_id':
#             stanza_id = v
#             continue
#        #if k == 'key':
#        #    key = v
#        #    continue
#        arg[k] = v
#
#    returnValue = ibmsecurity.isam.web.reverse_proxy.configuration.stanza.delete(iviaServer, inst_name, stanza_id, **arg)
#    logging.log(logging.INFO, returnValue)
#
#    if returnValue is not None:
#        assert not returnValue.failed()
