import logging

import ibmsecurity.isam.base.admin
import ibmsecurity.isam.appliance


def test_get_base_admin(iviaServer, caplog) -> None:
    """Get all admincfg options."""
    caplog.set_level(logging.DEBUG)

    returnValue = ibmsecurity.isam.base.admin.get(isamAppliance=iviaServer)
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()


def test_set_base_admin(iviaServer, caplog) -> None:
    """Set some admincfg options."""
    caplog.set_level(logging.DEBUG)

    returnValue = ibmsecurity.isam.base.admin.set(isamAppliance=iviaServer, force=False, minHeapSize=128, maxHeapSize=2048, sessionTimeout=720, httpPort=None, httpsPort=443, minThreads=None, maxThreads=None, maxPoolSize=100, lmiDebuggingEnabled=None, consoleLogLevel="OFF", acceptClientCerts=False, validateClientCertIdentity=True, excludeCsrfChecking=None, maxFiles=2, maxFileSize=20, enabledTLS=['TLSv1.2'], sshdPort=22, sessionCachePurge=120, sessionInactivityTimeout=90, enabledServerProtocols="TLSv1.2", loginHeader="IBM TEST", loginMessage="Ansible Me", baSessionTimeout=300, accessLogFormat="client=%h user=%u time=%t request=\"%r\" status=%s http_user_agent=\"%{User-Agent}\"", jsVersion="")
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
