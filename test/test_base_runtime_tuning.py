import logging

import ibmsecurity.isam.base.runtime.tuning_parameters
import ibmsecurity.isam.appliance

import pytest

def getTestData():
    testdata = [
        {
            "values": {
                "trace_specification": "*=info",
                "accept_client_certs": False,
                "require_mtls": False,
                "enabled_server_protocols": "TLSv1.2",
                "enable_sso": False,
                "auto_restart": False,
                "auto_reload": False,
                "console_log_level": "OFF",
                "suppress_sensitive_trace": False,
                "session_max_count": 1000,
                "session_invalidation_timeout": 1800,
                "session_reaper_poll_interval": 30,
                "max_heap_size": 1024,
                "min_heap_size": 512,
                "max_threads": 20,
                "min_threads": 10,
                "max_files": 2,
                "max_file_size": 40,
                "enable_crldp": False,
                "dns_resolution_cache_lifetime": 604800,
                "keystore": "rt_profile_keys",
                "keystore_label": "server",
                "truststore": "rt_profile_keys",
                "inbound_keystore":"rt_profile_keys",
                "inbound_keystore_label": "server",
                "inbound_truststore": "rt_profile_keys"
            }
        },
        {
            "option": "enable_crldp",
            "value": True
        },
        {
            "option": "max_files",
            "value": 2
        },
        {
            "values": {
                "trace_specification": "*=info",
                "accept_client_certs": False,
                "require_mtls": False,
                "enabled_server_protocols": "TLSv1.2",
                "enable_sso": False,
                "auto_restart": False,
                "auto_reload": False,
                "console_log_level": "OFF",
                "suppress_sensitive_trace": False,
                "session_max_count": 1000,
                "session_invalidation_timeout": 1800,
                "session_reaper_poll_interval": 30,
                "enable_crldp": True,
                "dns_resolution_cache_lifetime": 604800,
                "keystore": "rt_profile_keys",
            }
        },
    ]
    return testdata


@pytest.mark.parametrize("items", getTestData())
def test_set_multiple_tuning_parameeters(iviaServer, caplog, items) -> None:
    """Set api protection"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    option = None
    value = None

    for k, v in items.items():
        if k == 'option':
            option = v
            continue
        if k == 'value':
            value = v
            continue
        arg[k] = v

    returnValue = ibmsecurity.isam.base.runtime.tuning_parameters.set(iviaServer,
                                                                      option,
                                                                      value,
                                                                      **arg
                                                                      )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
