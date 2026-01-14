import logging
import pytest

import ibmsecurity.isam.base.remote_syslog.forwarder
import ibmsecurity.isam.appliance

def getTestData():
    testdata = [
        {
          "port": "514",
          "protocol": "tcp",
          "server": "rsyslog",
          "sources": [
           {"facility": "local0",
            "name": "WebSEAL:default:msg__webseald-default.log",
            "severity": "info",
            "tag": "webseal"},
           {"facility": "local0",
            "name": "WebSEAL:default:request.log",
            "severity": "info",
            "tag": "request"},
            ]
        },
        {
            "port": 6514,
            "protocol": "udp",
            "server": "rsyslog",
            "sources": [
                {"facility": "local0",
                 "name": "WebSEAL:default:msg__webseald-default.log",
                 "severity": "info",
                 "tag": "webseal2"},
                {"facility": "local0",
                 "name": "WebSEAL:default:request.log",
                 "severity": "info",
                 "tag": "request2"},
            ]
        },
    ]
    return testdata


@pytest.mark.parametrize("items", getTestData())
def test_set_remote_syslog_forwarder(iviaServer, caplog, items) -> None:
    """Get tracing protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}
    for k, v in items.items():
        arg[k] = v

    returnValue = ibmsecurity.isam.base.remote_syslog.forwarder.set(iviaServer,
                                                     **arg
                                                    )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
